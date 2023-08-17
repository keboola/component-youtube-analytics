"""
Template Component main class.

"""
import logging
import os
import time
import csv

from keboola.component.base import ComponentBase, sync_action
from keboola.component.exceptions import UserException
from keboola.component.sync_actions import SelectElement
from configuration import Configuration, InputVariantEnum
from google_yt.client import Client
from report_types import report_types
from googleapiclient.errors import HttpError


class Component(ComponentBase):
    """
        Extends base class for general Python components. Initializes the CommonInterface
        and performs configuration validation.

        For easier debugging the data folder is picked up by default from `../data` path,
        relative to working directory.

        If `debug` parameter is present in the `config.json`, the default logger is set to verbose DEBUG mode.

        The extractor algorithm is documented under the Component.run(self) method.
    """

    def __init__(self):
        super().__init__()
        self.conf = None
        self.client_yt = None

    @property
    def client(self) -> Client:
        """Retrieve google client for communication to the YT reporting service.

        If this is the first access to a client, application tries to create it. There are two options available:
        1) Create a client just by supplying an access token found in parameters as '#api_token'.
            It is used just during development when OAuth2 was not yet provided.
        2) Create a client using OAuth credentials from component configuration.
            This option ignores 'access_token'. It always creates a new token from a 'refresh_token'
        """
        if not self.client_yt:
            user = passwd = ''
            token_data = None
            api_token = self.configuration.parameters.get('#api_token')
            if not api_token:
                user = self.configuration.oauth_credentials.appKey
                passwd = self.configuration.oauth_credentials.appSecret
                token_data = {
                    'expires_at': 22222,
                    'access_token': 'neverusedcanbeanything',
                    'refresh_token': self.configuration.oauth_credentials.data.get('refresh_token'),
                    'token_type': 'Bearer'
                }
            self.client_yt = Client(access_token=api_token, client_id=user, app_secret=passwd, token_data=token_data)
        return self.client_yt

    def run(self):
        """Main execution code

        1) Initialize Configurtion based on parameters section of component configuration

        2) Retrieve state information on running the component.
            The state comprises information of last run of the component:
            - onBehalfOfContentOwner .. ID of content owner if explicit owner was used
            - jobs .. mapping of report_type_id to existing jobs.
                Each job contains following fields:
                - created .. True / False flag indicating whether the job was created by the component
                - id .. ID of the job
                - lastReportCreateTime .. used as a filter to optimize number of requests to the API

        3) State cleanup
            Remove jobs that were created by the component but that are not requested in current run.
            (because of a change in component configuration)

        4) Create needed job(s)
            If a report type is requested for which there is no job in the system then such a job is created.

        5) Download reports
            For each requested report type check whether there were new report data available.
            When there are new report(s) for specific reporty type then collect most up-to-date information
            and prepare incremental output table for it.

        6) Write new state
        """

        # 1) Initialize Configuration
        params = self.configuration.parameters
        self.conf = Configuration.fromDict(parameters=params)

        # Check configuration validity - report problem early
        if not self.conf.report_types:
            raise UserException('Configuration has no report types specified')
        if self.conf.input_variant == InputVariantEnum.use_selected_owner and not self.conf.content_owner:
            raise UserException('Configuration assumes explicit content owner but none is specified')

        # Normalize configuration
        if self.conf.input_variant is not InputVariantEnum.use_selected_owner:
            self.conf.content_owner = ''

        # 2) Retrieve state - get last state data/in/state.json from previous run
        previous_state = self.get_state_file()
        logging.debug(f'Original state: {previous_state}')

        # normalize state to a compatible version
        if 'onBehalfOfContentOwner' not in previous_state:
            previous_state['onBehalfOfContentOwner'] = ''
        if 'jobs' not in previous_state:
            previous_state['jobs'] = dict()

        # 3) Cleanup - remove created (by this configuration) jobs that are not requested
        for key, job in previous_state['jobs'].items():
            if not job.get('created'):
                continue  # we do not remove a job that we did not have created
            if self.conf.content_owner is not previous_state['onBehalfOfContentOwner'] or \
                    key not in self.conf.report_types:
                self.client.delete_job(job_id=job['id'], on_behalf_of_owner=previous_state['onBehalfOfContentOwner'])

        all_jobs = self.client.list_jobs(on_behalf_of_owner=self.conf.content_owner)

        new_state = {
            "onBehalfOfContentOwner": self.conf.content_owner,
            "jobs": dict()
        }

        # 4) Create needed jobs
        for report_type_id in self.conf.report_types:
            # search corresponding job among all available jobs
            job_created = False
            job = next(filter(lambda x: x['reportTypeId'] == report_type_id, all_jobs), None)
            if not job:
                job = self.client.create_job(f'keboola_{report_type_id}',
                                             report_type_id=report_type_id,
                                             on_behalf_of_owner=self.conf.content_owner)
                job_created = True
            job_from_state = previous_state['jobs'].get(report_type_id)
            if job_from_state and job_from_state['id'] == job['id']:
                new_state['jobs'][report_type_id] = job_from_state
            else:
                new_state['jobs'][report_type_id] = job
                job['created'] = job_created

        # 5) Download reports
        for job in new_state['jobs'].values():
            self.process_job(job)

        # 6) Write new state
        self.write_state_file(new_state)

    def process_job(self, job):
        """Process reports associated with a job

        There is one job for each report_type_id. There may be more reports associated with a job.
        Each report comprises data for one 24hour period. System may generate more than one report
        for each 24hour period. It makes sense to consider only the latest (report's createTime)
        report associated with specific 24hour period.

        job attributes:
            - created: boolean - flag whether the job was created by this configuration
            - id: str - job ID as maintained by the system
            - reportTypeId: str - system information
            - name: str - arbitrary name of the job
            - createTime: str - system information about the job (example: "2023-08-01T21:36:11Z")
            - lastReportCreateTime": str - information about last retrieved report

        """

        # Retrie reports that were not processed yet (if no state info available then request all)
        logging.debug(f'Processing job: {job.get("reportTypeId")}')
        last_report_create_time = job.get('lastReportCreateTime')
        reports = self.client.list_reports(job_id=job['id'], created_after=last_report_create_time)
        if not reports:
            return

        logging.debug(f'   Number of reports to be processed: {len(reports)}')

        # Prepare output table description (manifest)
        report_type_id = job['reportTypeId']
        table_def = self.create_out_table_definition(f'{report_type_id}.csv',
                                                     incremental=True,
                                                     is_sliced=True,
                                                     primary_key=report_types[report_type_id]['dimensions']
                                                     )
        os.makedirs(table_def.full_path, exist_ok=True)

        report_raw_full_path = f'{self.files_out_path}/{report_type_id}.csv'
        os.makedirs(report_raw_full_path, exist_ok=True)

        # self.write_manifest(table_def)

        # Retrieve create time of the latest available report and store it in the new state
        reports = sorted(reports, key=lambda d: d['createTime'], reverse=True)
        job['lastReportCreateTime'] = reports[0]['createTime']
        # Sort list of reports based on data period (startTime) and then on creation time (createTime).
        reports = sorted(reports, key=lambda d: d['startTime'] + d['createTime'])
        for index in range(len(reports)):
            report = reports[index]
            # Consider only the last report among a set of reports for specific data period
            if index + 1 == len(reports) or report['startTime'] != reports[index + 1]['startTime']:
                filename_raw = f'{report_raw_full_path}/{report["startTime"].replace(":", "_")}.csv'
                filename_tgt = f'{table_def.full_path}/{report["startTime"].replace(":", "_")}.csv'
                self.write_report(filename_raw, report['downloadUrl'])
                if not table_def.columns:
                    columns = self._read_columns(filename_raw)
                    table_def.columns = columns
                self._strip_header(filename_raw, filename_tgt)

        self.write_manifest(table_def)

    @staticmethod
    def _read_columns(filename) -> list:
        with open(filename) as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',')
            header = next(csvreader)
            return header

    @staticmethod
    def _strip_header(filename_raw, filename_tgt):
        with open(filename_raw, mode='rt') as src, open(filename_tgt, mode='wt') as tgt:
            src.readline()
            while True:
                row = src.readline()
                if not row:
                    break
                tgt.write(row)
        pass

    def write_report(self, filename, downloadUrl):
        """Download a report from media URL to target CSV file
        """
        while True:
            try:
                self.client.read_report_file(filename, downloadUrl)
                return
            except HttpError as error:
                if error.status_code == 429:
                    logging.debug(f'Quota limit exceeded reading {filename}')
                    time.sleep(30)
                    logging.debug(f'Resuming {filename}')
                else:
                    raise error

    # Eventually we opted not to read report type ids dynamically.
    # Instead, we just use fixed set of types as retrieved from the API documentation.
    # @sync_action('list_report_types')
    # def list_report_types(self):
    #     report_type_ids = self.client.list_report_types()
    #     results = [SelectElement(value=tid['id'], label=f"{tid['name']} ({tid['id']})") for tid in report_type_ids]
    #     return results


"""
        Main entrypoint
"""
if __name__ == "__main__":
    try:
        comp = Component()
        # this triggers the run method by default and is controlled by the configuration.action parameter
        comp.execute_action()
    except UserException as exc:
        logging.exception(exc)
        exit(1)
    except Exception as exc:
        logging.exception(exc)
        exit(2)

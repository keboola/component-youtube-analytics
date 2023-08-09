"""
Template Component main class.

"""
import csv
import logging
from datetime import datetime

from keboola.component.base import ComponentBase
from keboola.component.exceptions import UserException
from configuration import Configuration, InputVariantEnum
from google_yt.client import Client

# configuration variables
KEY_API_TOKEN = '#api_token'
KEY_PRINT_HELLO = 'print_hello'

# list of mandatory parameters => if some is missing,
# component will fail with readable message on initialization.
REQUIRED_PARAMETERS = [KEY_PRINT_HELLO]
REQUIRED_IMAGE_PARS = []


class Component(ComponentBase):
    """
        Extends base class for general Python components. Initializes the CommonInterface
        and performs configuration validation.

        For easier debugging the data folder is picked up by default from `../data` path,
        relative to working directory.

        If `debug` parameter is present in the `config.json`, the default logger is set to verbose DEBUG mode.
    """

    def __init__(self):
        super().__init__()
        self.client_yt = None
        self.conf: Configuration = None

    @property
    def client(self):
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
        """
        Main execution code
        """

        params = self.configuration.parameters
        self.conf = Configuration.fromDict(parameters=params)

        # Check configuration - report problem early
        if not self.conf.report_types:
            raise UserException('Configuration has no report types specified')
        if self.conf.input_variant == InputVariantEnum.use_selected_owner and not self.conf.content_owner:
            raise UserException('Configuration assumes explicit content owner but none is specified')

        # Normalize configuration
        if self.conf.input_variant is not InputVariantEnum.use_selected_owner:
            self.conf.content_owner = ''

        # get last state data/in/state.json from previous run
        previous_state = self.get_state_file()
        logging.debug(f'Original state: {previous_state}')

        # normalize state to a compatible version
        if 'onBehalfOfContentOwner' not in previous_state:
            previous_state['onBehalfOfContentOwner'] = ''
        if 'jobs' not in previous_state:
            previous_state['jobs'] = dict()

        # TODO: Remove the code - it is just for development
        for job in previous_state['jobs'].values():
            self.process_job(job)

        # Cleanup - remove created (by this configuration) jobs that are not requested
        for key, job in previous_state['jobs'].items():
            if not job.get('created'):
                continue  # we do not remove a job that we did not have created
            if self.conf.content_owner is not previous_state['onBehalfOfContentOwner'] or \
                    key not in self.conf.report_types:
                self.client.delete_job(on_behalf_of_owner=previous_state['onBehalfOfContentOwner'])

        all_jobs = self.client.list_jobs(on_behalf_of_owner=self.conf.content_owner)

        # Make sure that there is a job for each requested report type.
        # When a job is missing it is created.
        #
        new_state = {
            "onBehalfOfContentOwner": self.conf.content_owner,
            "jobs": dict()
        }
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

        for job in new_state['jobs']:
            self.process_job(job)

        # Create output table (Tabledefinition - just metadata)
        table = self.create_out_table_definition('output.csv', incremental=True, primary_key=['timestamp'])

        # get file path of the table (data/out/tables/Features.csv)
        out_table_path = table.full_path
        logging.info(out_table_path)

        # DO whatever and save into out_table_path
        with open(table.full_path, mode='wt', encoding='utf-8', newline='') as out_file:
            writer = csv.DictWriter(out_file, fieldnames=['timestamp'])
            writer.writeheader()
            writer.writerow({"timestamp": datetime.now().isoformat()})

        # Save table manifest (output.csv.manifest) from the tabledefinition
        self.write_manifest(table)

        # Write new state - will be available next run
        self.write_state_file({"some_state_parameter": "value"})

    def process_job(self, job):
        """
        job attributes:
            created: boolean - flag whether the job was created by this configuration
            id: str - job ID as maintained by the system
            reportTypeId: str - system information
            name: str - arbitrary name of the job
            createTime: str - system information (example: "2023-08-01T21:36:11Z")
            lastReport": object - information about last retrieved report
                id: str - report ID (example: "8630070020")
                startTime: str - start of reported period (example: "2023-06-26T07:00:00Z")
                endTime: str - end of reported period (example: "2023-06-27T07:00:00Z")
                createTime: str - time of report creation (example: "2023-07-26T07:36:39.102883Z")

        """
        last_report_create_time = job['lastReport']['createTime'] if 'lastReport' in job else None
        reports = self.client.list_reports(job_id=job['id'], created_after=last_report_create_time)
        reports = sorted(reports, key=lambda d: d['createTime'])
        last_written = None
        for index in range(len(reports)):
            report = reports[index]
            if index+1 == len(reports) or report['endTime'] != reports[index+1]['endTime']:
                filename = report['endTime']+'.csv'
                filename = filename.replace(':', '_')
                self.write_report(filename, report['downloadUrl'])
                last_written = report

        if last_written:
            # TODO: Instead of explicit dict construction use dict operations (exclue / include) against report
            job['lastReport'] = {
                'id': report['id'],
                'createTime': report['createTime']
            }

    def write_report(self, filename, downloadUrl):
        self.client.read_report_file(filename, downloadUrl)
        # TODO: read response - we probably do not need it ...
        pass

        # ####### EXAMPLE TO REMOVE END


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

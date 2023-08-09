from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
import io

SCOPES = ['https://www.googleapis.com/auth/yt-analytics-monetary.readonly']
API_SERVICE_NAME = 'youtubereporting'
API_VERSION = 'v1'


class Client:

    def __init__(self, access_token: str = None, client_id: str = None, app_secret: str = None,
                 token_data: dict = None):
        self.service = None
        if access_token:
            credentials = Credentials(token=access_token)
            pass
        else:
            client_secrets = {
                "web": {
                    "client_id": client_id,
                    "client_secret": app_secret,
                    "redirect_uris": ["https://www.example.com/oauth2callback"],
                    "auth_uri": "https://oauth2.googleapis.com/auth",
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
            }
            credentials = Flow.from_client_config(client_secrets, scopes=SCOPES, token=token_data).credentials
        self.service = build(serviceName=API_SERVICE_NAME,
                             version=API_VERSION,
                             credentials=credentials)
        pass

    def list_report_types(self, on_behalf_of_owner='', include_system_managed=False):
        """Returns a list of report types that the channel or content owner can retrieve

        Uses API: https://developers.google.com/youtube/reporting/v1/reference/rest/v1/reportTypes/list

        """
        kwargs = dict()
        if on_behalf_of_owner:
            kwargs['onBehalfOfContentOwner'] = on_behalf_of_owner
        if include_system_managed:
            kwargs['includeSystemManaged'] = include_system_managed
        results = self.service.reportTypes().list(**kwargs).execute()
        return results.get('reportTypes')

    def create_job(self, name: str, report_type_id: str, on_behalf_of_owner=''):
        """Create a job for specific report type.

        Uses API: https://developers.google.com/youtube/reporting/v1/reference/rest/v1/jobs/create

        API does not allow to create a 'systemManaged' job explicitly as it is already created by the system.
        (It is not allowed to specify a report type that is system managed)

        Args:
            name: Name of the job (maximum 100 characters)
            report_type_id: ID of a report type as listed by list_report_types(...)
            on_behalf_of_owner: If specified then specific channel owner reports will be listed.

        Returns:
            Job resource. Example
                {
                    'id': '5ce37f48-f2b6-4eaa-a0c5-afe6d4927f2a',
                    'reportTypeId': string,
                    'name': 'channel_cards_a1',
                    'createTime': '2023-08-01T21:22:27.501838Z',
                    'expireTime': timestamp,  # optional
                    'systemManaged': boolean  # optional
                }

        Raises:
            HttpError 400 - Bad Request - missing name or missing or non-existing report_type_id, or depricated
                403 - Forbidden - attempt to create system managed report
                409 - Conflict - resource already exists


        """
        body = {
            'name': name,
            'reportTypeId': report_type_id
        }
        kwargs = dict()
        if on_behalf_of_owner:
            kwargs['onBehalfOfContentOwner'] = on_behalf_of_owner
        results = self.service.jobs().create(body=body, **kwargs).execute()
        return results

    def delete_job(self, job_id: str, on_behalf_of_owner=''):
        """Delete existing job

        Uses API: https://developers.google.com/youtube/reporting/v1/reference/rest/v1/jobs/delete

        """
        # TODO: complete method documentation
        kwargs = {}
        if on_behalf_of_owner:
            kwargs['onBehalfOfContentOwner'] = on_behalf_of_owner
        try:
            results = self.service.jobs().delete(jobId=job_id, **kwargs).execute()
        except HttpError as ex:
            # we allow for non-existent job, other errors will be propagated
            if ex.status_code != 404:
                raise ex


    def list_jobs(self, on_behalf_of_owner: str = '', include_system_managed=False):
        """List jobs

        Uses API: https://developers.google.com/youtube/reporting/v1/reference/rest/v1/jobs/list

        Args:
            on_behalf_of_owner: If specified then specific channel owner reports will be listed.
                If not specified then current user channel reports will be listed.
            include_system_managed: If specified and True then system managed jobs will be listed.

        Returns:
            A list of retrieved jobs. Example:
            [
               {
                'id': ''7a25fac7-a579-46ba-9aa2-6349600bd6eb'',
                'reportTypeId': 'channel_basic_a2',
                'name': 'basic_test',
                'createTime': '2023-07-31T04:47:02.012627Z'
               },
               ...
            ]
        """
        kwargs = {}
        if on_behalf_of_owner:
            kwargs['onBehalfOfContentOwner'] = on_behalf_of_owner
        if include_system_managed:
            kwargs['includeSystemManaged'] = include_system_managed

        results = self.service.jobs().list(**kwargs).execute()
        return results.get('jobs')

    def list_reports(self, job_id: str, on_behalf_of_owner: str = '', created_after: str = ''):
        """List reports associated with specified job

        Uses API: https://developers.google.com/youtube/reporting/v1/reference/rest/v1/jobs.reports/list

        Args:
            job_id: ID of a job - must be specified
            on_behalf_of_owner: If specified then specific channel owner reports will be listed.
                If not specified then current user channel reports will be listed.
            created_after: Filter only reports newer than specified date.
                It is the best practice to specify value of createTime of latest retrieved report.

        Returns:
            A list of retrieved reports. Example:
            [
               {
                'id': '8652265865',
                'jobId': '7a25fac7-a579-46ba-9aa2-6349600bd6eb',
                'startTime': '2023-07-29T07:00:00Z',
                'endTime': '2023-07-30T07:00:00Z',
                'createTime': '2023-07-31T04:47:02.012627Z',
                'downloadUrl': 'https://youtubereporting.googleapis.com/.../jobs/7a2...6eb/reports/86...65?alt=media'
               },
               ...
            ]

        """
        kwargs = dict()
        if on_behalf_of_owner:
            kwargs['onBehalfOfContentOwner'] = on_behalf_of_owner
        if created_after:
            kwargs['createdAfter'] = created_after
        reports = []
        while True:
            results = self.service.jobs().reports().list(jobId=job_id, **kwargs).execute()
            if 'reports' not in results:
                break  # if there were no reports yet, there is no reports list at all
            reports.extend(results['reports'])
            if 'nextPageToken' not in results:
                break  # There are no more data, leave the loop
            kwargs['pageToken'] = results['nextPageToken']

        return reports

    def get_report(self, job_id: str, report_id: str, **kwargs):
        results = self.service.jobs().reports().get(jobId=job_id, reportId=report_id, **kwargs).execute()
        return results

    def read_report_file(self, filename: str, downloadUrl: str):
        request = self.service.media().download_media(resourceName='')
        request.uri = downloadUrl
        out_file = io.FileIO(filename, mode='wb')
        downloader = MediaIoBaseDownload(out_file, request, chunksize=8192)
        download_finished = False
        while download_finished is False:
            _, download_finished = downloader.next_chunk()
        pass


if __name__ == '__main__':
    import os

    ACCESS_TOKEN_EXAMPLE = os.environ['ACCESS_TOKEN_EXAMPLE']
    REFRESH_TOKEN_EXAMPLE = os.environ['REFRESH_TOKEN_EXAMPLE']
    CLIENT_ID_EXAMPLE = os.environ['CLIENT_ID_EXAMPLE']
    CLIENT_SECRET_EXAMPLE = os.environ['CLIENT_SECRET_EXAMPLE']

    token_data_example = {
        'expires_at': 22222,
        'access_token': 'neverusedcanbeanything',
        'refresh_token': REFRESH_TOKEN_EXAMPLE,
        'token_type': 'Bearer'
    }

    # client = Client(client_id=CLIENT_ID_EXAMPLE,
    #                 app_secret=CLIENT_SECRET_EXAMPLE,
    #                 token_data=token_data_example)
    client = Client(access_token=ACCESS_TOKEN_EXAMPLE)

    # result = client.list_report_types(include_system_managed=False)
    # print(f'Number of report types: {len(result)}')
    # for item in result:
    #     # print(item['id'], item['name'])
    #     print(item)

    # result = client.create_job(name='my_province_druha', report_type_id='channel_province_a2')
    # print(f'JOB CREATED: {result}')

    result = client.list_jobs(include_system_managed=False)
    print(f'Number of jobs: {len(result)}')
    for item in result:
        # print(item['id'], item['name'], item['reportTypeId'])
        print(item)
    #     reports = client.list_reports(item['id'])
    #     for report in reports:
    #         print(f'   {report}')
    # filename = f'C:\\Users\\DK\\Revolt\\Projects\\kds-team.ex-youtube-analytics\\data\\' \
    #            f'out/tmp/{item["reportTypeId"]}_{report["createTime"].replace(":","-")}.csv'
    # client.read_report_file(filename, report['downloadUrl'])

    # result = client.list_reports('7a25fac7-a579-46ba-9aa2-6349600bd6eb', created_after='2023-07-26T07:41:15.298797Z')
    # print(len(result))
    # for report in result:
    #     print(report)

    # result = client.get_report(job_id='7a25fac7-a579-46ba-9aa2-6349600bd6eb', report_id='8652265865')
    #
    # client.read_report_file('output.txt', downloadUrl=result['downloadUrl'])

    # client.delete_job(job_id='12443452')

    pass

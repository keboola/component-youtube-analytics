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
        return results

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

    def read_report_file(self, filename: str, downloadUrl: str):
        """Download generated report (specified by media URL) into a local file.

        GCP library provides dedicated method to download a stream of data into a local file.
        """
        request = self.service.media().download_media(resourceName='')
        request.uri = downloadUrl

        with io.FileIO(filename, mode='wb') as out_file:
            downloader = MediaIoBaseDownload(out_file, request, chunksize=8192)
            download_finished = False
            while download_finished is False:
                _, download_finished = downloader.next_chunk(num_retries=4)
            pass

import io
from functools import wraps

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from keboola.component.exceptions import UserException

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
                    "auth_uri": "https://oauth2.googleapis.com/auth",
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
            }
            # make sure the token is expired explicitly to force refresh
            token_data['expires_at'] = 0
            credentials = Flow.from_client_config(client_secrets, scopes=SCOPES, token=token_data).credentials
        self.service = build(serviceName=API_SERVICE_NAME,
                             version=API_VERSION,
                             credentials=credentials)
        pass

    @staticmethod
    def handle_http_error(func):
        """Handle Http communication errors in a uniform manner

        It is used as a decorator. If the decorated function is called with context_description named parameter
        its contents will be used in UserException message.

        Raises:
            Exception: HttpError will be converted to UserException using context_description parameter
        """

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            context_description = kwargs.get('context_description') if 'context_description' in kwargs else ''
            try:
                result = func(self, *args, **kwargs)
                return result
            except HttpError as error:
                raise UserException(f'{context_description} - Http error {error.status_code}: {error.reason}')
            except Exception:
                raise

        return wrapper

    @handle_http_error
    def list_report_types(self, on_behalf_of_owner='', include_system_managed=False, context_description=''):
        """Returns a list of report types that the channel or content owner can retrieve

        Uses API: https://developers.google.com/youtube/reporting/v1/reference/rest/v1/reportTypes/list

        Args:
            on_behalf_of_owner: explicit content owner
            include_system_managed: flag to include system managed types - we never use it actually
            context_description: text that will be used in handle_http_error decorator
        """
        kwargs = dict()
        if on_behalf_of_owner:
            kwargs['onBehalfOfContentOwner'] = on_behalf_of_owner
        if include_system_managed:
            kwargs['includeSystemManaged'] = include_system_managed
        results = self.service.reportTypes().list(**kwargs).execute()
        return results.get('reportTypes')

    @handle_http_error
    def create_job(self, name: str, report_type_id: str, on_behalf_of_owner='', context_description=''):
        """Create a job for specific report type.

        Uses API: https://developers.google.com/youtube/reporting/v1/reference/rest/v1/jobs/create

        API does not allow to create a 'systemManaged' job explicitly as it is already created by the system.
        (It is not allowed to specify a report type that is system managed)

        Args:
            name: Name of the job (maximum 100 characters)
            report_type_id: ID of a report type as listed by list_report_types(...)
            on_behalf_of_owner: If specified then specific channel owner reports will be listed
            context_description: text that will be used in handle_http_error decorator

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

    @handle_http_error
    def delete_job(self, job_id: str, on_behalf_of_owner='', context_description=''):
        """Delete existing job

        Uses API: https://developers.google.com/youtube/reporting/v1/reference/rest/v1/jobs/delete

        Args:
            job_id: ID of a job to delete
            on_behalf_of_owner: If specified then specific channel owner reports will be listed
            context_description: text that will be used in handle_http_error decorator
        """
        kwargs = {}
        if on_behalf_of_owner:
            kwargs['onBehalfOfContentOwner'] = on_behalf_of_owner
        try:
            self.service.jobs().delete(jobId=job_id, **kwargs).execute()
        except HttpError as ex:
            # we allow for non-existent job, other errors will be propagated
            if ex.status_code != 404:
                raise
        return

    @handle_http_error
    def list_jobs(self, on_behalf_of_owner: str = '', include_system_managed=False, context_description=''):
        """List jobs

        Uses API: https://developers.google.com/youtube/reporting/v1/reference/rest/v1/jobs/list

        Args:
            on_behalf_of_owner: If specified then specific channel owner reports will be listed.
                If not specified then current user channel reports will be listed.
            include_system_managed: If specified and True then system managed jobs will be listed.
            context_description: text that will be used in handle_http_error decorator

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
        return results.get('jobs', [])

    @handle_http_error
    def list_reports(self, job_id: str, on_behalf_of_owner: str = '', created_after: str = '',
                     context_description=''):
        """List reports associated with specified job

        Uses API: https://developers.google.com/youtube/reporting/v1/reference/rest/v1/jobs.reports/list

        Args:
            job_id: ID of a job - must be specified
            on_behalf_of_owner: If specified then specific channel owner reports will be listed.
                If not specified then current user channel reports will be listed.
            created_after: Filter only reports newer than specified date.
                It is the best practice to specify value of createTime of latest retrieved report.
            context_description: text that will be used in handle_http_error decorator

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

    @handle_http_error
    def download_report_file(self, downloadUrl: str, filename: str, context_description=''):
        """Download generated report (specified by media URL) into a local file.

        GCP library provides dedicated method to download a stream of data into a local file.

        Args:
            downloadUrl: URL providing report data
            filename: Target file where to write the data
            context_description: text that will be used in handle_http_error decorator
        """
        request = self.service.media().download_media(resourceName='')
        request.uri = downloadUrl

        with io.FileIO(filename, mode='wb') as out_file:
            downloader = MediaIoBaseDownload(out_file, request)
            download_finished = False
            while download_finished is False:
                _, download_finished = downloader.next_chunk(num_retries=15)
            pass

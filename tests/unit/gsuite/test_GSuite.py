from unittest                       import TestCase
from google.oauth2.credentials      import Credentials
from googleapiclient.discovery      import Resource
from osbot_utils.utils.Env          import load_dotenv
from osbot_gsuite.gsuite.GSuite     import GSuite


class test_GSuite(TestCase):

        @classmethod
        def setUpClass(cls):
            load_dotenv()
            cls.gsuite = GSuite()

        def test_create_credentials(self):
            with self.gsuite as _:
                credentials = self.gsuite.create_credentials()
                assert type(credentials)           is Credentials
                assert credentials.token_uri       == 'https://oauth2.googleapis.com/token'
                assert credentials.universe_domain == 'googleapis.com'

        def test_create_service(self):
            with self.gsuite as _:
                service = _.create_service('drive', 'v3', 'drive')
                assert type(service)          is Resource
                assert service._baseUrl       == "https://www.googleapis.com/drive/v3/"
                assert service._dynamic_attrs == ['new_batch_http_request', 'about', 'apps', 'changes', 'channels', 'comments', 'drives', 'files', 'operation', 'operations', 'permissions', 'replies', 'revisions', 'teamdrives']

        def test_admin_reports_v1(self):
            with self.gsuite as _:
                service = _.admin_reports_v1()
                assert type(service)          is Resource
                assert service._baseUrl       == "https://admin.googleapis.com/"
                assert service._dynamic_attrs == ['new_batch_http_request', 'activities', 'channels', 'customerUsageReports', 'entityUsageReports', 'userUsageReport']

        def test_calendar_v3(self):
            with self.gsuite as _:
                service = _.calendar_v3()
                assert type(service)          is Resource
                assert service._baseUrl       == 'https://www.googleapis.com/calendar/v3/'
                assert service._dynamic_attrs == ['new_batch_http_request', 'acl', 'calendarList', 'calendars', 'channels', 'colors', 'events', 'freebusy', 'settings']

        def test_docs_v1(self):
            with self.gsuite as _:
                service = _.docs_v1()
                assert type(service)          is Resource
                assert service._baseUrl       == 'https://docs.googleapis.com/'
                assert service._dynamic_attrs == ['new_batch_http_request', 'documents']

        def test_drive_v3(self):
            with self.gsuite as _:
                service = _.drive_v3()
                assert type(service)          is Resource
                assert service._baseUrl       == 'https://www.googleapis.com/drive/v3/'
                assert service._dynamic_attrs == ['new_batch_http_request', 'about', 'apps', 'changes', 'channels', 'comments', 'drives', 'files', 'operation', 'operations', 'permissions', 'replies', 'revisions', 'teamdrives']

        def test_drive_activity_v2(self):
            with self.gsuite as _:
                service = _.drive_activity_v2()
                assert type(service)          is Resource
                assert service._baseUrl       == 'https://driveactivity.googleapis.com/'
                assert service._dynamic_attrs == ['new_batch_http_request', 'activity']

        def test_people_v1(self):
            with self.gsuite as _:
                service = _.people_v1()
                assert type(service)          is Resource
                assert service._baseUrl       == 'https://people.googleapis.com/'
                assert service._dynamic_attrs == ['new_batch_http_request', 'contactGroups', 'otherContacts', 'people']

        def test_slides_v1(self):
            with self.gsuite as _:
                service = _.slides_v1()
                assert type(service)          is Resource
                assert service._baseUrl       == 'https://slides.googleapis.com/'
                assert service._dynamic_attrs == ['new_batch_http_request', 'presentations']

        def test_sheets_v4(self):
            with self.gsuite as _:
                service = _.sheets_v4()
                assert type(service)          is Resource
                assert service._baseUrl       == 'https://sheets.googleapis.com/'
                assert service._dynamic_attrs == ['new_batch_http_request', 'spreadsheets']


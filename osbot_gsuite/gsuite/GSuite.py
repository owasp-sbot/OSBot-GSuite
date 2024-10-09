
from googleapiclient.discovery          import build
from google.oauth2.credentials          import Credentials
from googleapiclient.discovery          import Resource
from osbot_utils.utils.Json import json_loads

from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.utils.Env              import get_env

ENV_NAME__GSUITE__OAUTH2__DATA = 'GSUITE__OAUTH2__DATA'
ENV_NAME__GSUITE__OAUTH2__FILE = 'GSUITE__OAUTH2__FILE'


class GSuite(Type_Safe):                                           # todo see if there is a better name for this

    def gsuite__oauth2__data(self):
        return get_env(ENV_NAME__GSUITE__OAUTH2__DATA)

        # return file with token credentials
    def gsuite__oauth2__file(self):
        return get_env(ENV_NAME__GSUITE__OAUTH2__FILE)


    # this creates the credentials object required to create the GSuite service object
    def create_credentials(self, scopes=None) -> Credentials:
        oauth2_data = self.gsuite__oauth2__data()
        if oauth2_data:
            info        = json_loads(oauth2_data)
            credentials = Credentials.from_authorized_user_info(info, scopes=scopes)
            return credentials
        oauth2_file = self.gsuite__oauth2__file()
        if oauth2_file:
            credentials = Credentials.from_authorized_user_file(filename=oauth2_file, scopes=scopes)
            return credentials

        raise ValueError("no OAuth2 data or file found")


    def create_service(self,service_name, version, scopes) -> Resource:
        creds = self.create_credentials(scopes)
        return build(service_name, version, credentials=creds)

    # helper files to create individual GSuite service objects
    def admin_reports_v1(self):
        return self.create_service('admin', 'reports_v1','admin.reports.audit.readonly')

    def calendar_v3(self):
        return self.create_service('calendar','v3','calendar')

    def docs_v1(self):
        return self.create_service('docs', 'v1', 'documents')

    def drive_v3(self):
        kwargs = dict(service_name = 'drive',
                      version      = 'v3',
                      scopes       = ['https://www.googleapis.com/auth/drive'])
        return self.create_service(**kwargs)

    def drive_activity_v2(self):
        return self.create_service('driveactivity', 'v2', 'drive.activity')

    def people_v1(self):
        return self.create_service('people', 'v1', 'contacts')

    def slides_v1(self):
        return self.create_service('slides', 'v1', 'presentations')

    def sheets_v4(self):
        return self.create_service('sheets', 'v4', 'spreadsheets')


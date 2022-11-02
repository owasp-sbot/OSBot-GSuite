import json
import os

from httplib2                  import Http
from oauth2client              import file, client
from oauth2client.tools        import argparser
from oauth2client.tools        import run_flow

from googleapiclient.discovery import build
from osbot_aws.apis.Secrets import Secrets
from osbot_utils.utils.Files import Files, file_create, path_combine


class GSuite:
    def __init__(self, gsuite_secret_id=None):
        if gsuite_secret_id is None:
            self.gsuite_secret_id = 'gsuite_token'
        else:
            self.gsuite_secret_id = gsuite_secret_id

    # this function will prompt the user if there isn't a local tmp file with a token for the requested scope
    # the main credentials are stored using AWS Secrets (in the id defined at self.gsuite_secret_id)
    def get_oauth_token(self, desired_scope):
        #secret_data  = json.loads(Secrets(self.gsuite_secret_id).value())                           # load secret from AWS Secrets store
        file_token    = '/tmp/gmail_credential_{0}.json'.format(desired_scope)                          # this is the tmp file with the token value for the desired scope

        folder_auth = '/Users/diniscruz/_dev/_misc_data/'
        file_token = path_combine(folder_auth, 'file_token.json')


        if not Files.exists(file_token):                                                                # if the file does not existSecrets(self.gsuite_secret_id)
            token_data = Secrets(self.gsuite_secret_id).value()
            file_create(file_token, token_data)
            #if os.getenv('AWS_REGION') is not None or os.getenv('SYNC_SERVER'):                         # check if we are running in AWS or in the sync server
            #    Files.write(token_file, secret_data['token.json'])                                      # if we are, use the token.json value from the AWS secret_data
            # else:
            #     secret_data = json.loads(Secrets('gsuite_token').value())   # BUG, need to refactor this
            #     credentials_file = '/tmp/gsuite_credentials.json'                                       # file to hold the credentials.json value
            #     Files.write(credentials_file, secret_data['credentials.json'])                          # save value received from AWS into file
            #
            #     store         = file.Storage(token_file)                                                # create a gsuite Storage object
            #     scopes        = 'https://www.googleapis.com/auth/{0}'.format(desired_scope)             # full qualified name for the desired scopes
            #
            #     flow = client.flow_from_clientsecrets(credentials_file, scopes)                         # create a gsuite flow object
            #     flags = argparser.parse_args('--auth_host_name localhost --logging_level INFO'.split()) # configure the use of a localhost server to received the oauth response
            #     run_flow(flow, store, flags)                                                            # open browser and prompt user to follow the OAuth flow
            #
            #     Files.delete(credentials_file)                                                          # delete main gsuite credentials file (since we don't want it hanging around)

        return file_token                                                                           # return file with token credentials

    # this creates the credentials object required to create the GSuite service object
    def get_oauth_creds(self, desired_scope):
        #token_file = self.get_oauth_token(desired_scope)        # get the token file
        #store       = file.Storage(token_file)                  # create Storage object from file
        #creds       = store.get()                               # extract GSuite creds value

        from google.oauth2.credentials      import Credentials
        folder_auth = '/Users/diniscruz/_dev/_misc_data/'
        file_token = path_combine(folder_auth, 'file_token.json')

        creds = Credentials.from_authorized_user_file(file_token)

        return creds

    def create_service(self,serviceName, version, scope):
        creds = self.get_oauth_creds(scope)
        return build(serviceName, version, credentials=creds)
        #return build(serviceName, version, http=self.get_oauth_creds(scope).authorize(Http()))

    # helper files to create individual GSuite service objects
    def admin_reports_v1(self):
        return self.create_service('admin', 'reports_v1','admin.reports.audit.readonly')

    def calendar_v3(self):
        return self.create_service('calendar','v3','calendar')

    def docs_v1(self):
        return self.create_service('docs', 'v1', 'documents')

    def drive_v3(self):
        return self.create_service('drive', 'v3', 'drive')
        #return self.create_service('drive', 'v3', 'drive.metadata.readonly')

    def slides_v1(self):
        return self.create_service('slides', 'v1', 'presentations')

    def sheets_v4(self):
        return self.create_service('sheets', 'v4', 'spreadsheets')


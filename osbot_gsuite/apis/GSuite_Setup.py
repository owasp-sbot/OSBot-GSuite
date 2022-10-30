import os

from google_auth_oauthlib.flow      import InstalledAppFlow
from googleapiclient.discovery import build
from oauth2client                   import file, client
from oauth2client.tools             import argparser, run_flow
from google.oauth2.credentials      import Credentials
from google.auth.transport.requests import Request

from osbot_aws.apis.Secrets  import Secrets
from osbot_gsuite.apis.GSheets import GSheets
from osbot_gsuite.apis.GSlides import GSlides
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_not_exists, file_contents, file_create, path_combine
from osbot_utils.utils.Json import json_file_contents, file_create_json, json_dumps


class GSuite_Setup():

    def __init__(self):
        self.secret_id_gsuite_client_secret = 'gwbot_gsuite_client_secret'
        self.secret_id_gsuite_token         = 'gwbot_gsuite_token_2'

        #self.secret_id_with_credentials     = 'gsuite_token'
        #self.secret_id_to_create            = 'gsuite_gsbot_user'
        self.file_credentials               = '/tmp/gsuite_client_secret_{0}.json'.format(self.secret_id_gsuite_client_secret)  # todo: refactor to make it OS independent
        self.file_token                     = '/tmp/gmail_credential_{0}.json'    .format(self.secret_id_gsuite_token)

    # Create credentials at https://console.developers.google.com/apis/api/docs.googleapis.com/overview
    # and save them to local disk
    def save_gsuite_client_secret_in_aws(self, file_with_credentials):
        if file_not_exists(file_with_credentials):
            raise Exception(f'provided file does not exist: {file_with_credentials}')
        gwbot_gsuite_secret = file_contents(file_with_credentials)

        #if Secrets(self.secret_id_gsuite_client_secret).update_to_json_string(gwbot_gsuite_secret):        # bug: current privs for the aws account used doesn't have update privs for secrets
        #    return True
        if Secrets(self.secret_id_gsuite_client_secret).create(gwbot_gsuite_secret):
           return True

        raise Exception(f'cloud not update secret: {self.secret_id_gsuite_client_secret}')


    # note: double check thta the 'refresh_token' is set on the AWS Secret (if not, it will fail after a couple hours)
    # todo: figure out how long until then main token expires and Auth workflow is required again
    def create_auth_token_using_web_browser_flow(self, scopes):

        client_secret = Secrets(self.secret_id_gsuite_client_secret).value()                     # get client_secret from AWS Secrets
        store_token   = file.Storage(self.file_token)                                            # create storage object to save token

        file_create(self.file_credentials, client_secret)                                        # save it to temp file

        flow  = client.flow_from_clientsecrets(self.file_credentials, scopes)                    # create a gsuite flow object
        flags = argparser.parse_args('--auth_host_name localhost --logging_level INFO'.split())  # configure the use of a localhost server to received the oauth response
        run_flow(flow, store_token, flags)                                                       # open browser and prompt user to follow the OAuth flow, which will save the token data in self.file_token

        token_json = file_contents(self.file_token)                                              # get gsuite token contents
        Secrets(self.secret_id_gsuite_token).create(token_json)                                  # save it on AWS Secret
        # todo: fix code above to use .update instead of .create (current AWS account only has


    def create_auth_token_using_web_browser_flow__store_in_env(self, scopes):

        #client_secret = Secrets(self.secret_id_gsuite_client_secret).value()                     # get client_secret from AWS Secrets
        folder_auth      = '/Users/diniscruz/_dev/_misc_data/'
        gsuite_auth_file = path_combine(folder_auth, 'client_secret____.apps.googleusercontent.com.json')
        file_credentials = path_combine(folder_auth, 'file_credentials.json')
        file_token       = path_combine(folder_auth, 'file_token.json')

        creds = None

        if os.path.exists(file_token):
            creds = Credentials.from_authorized_user_file(file_token, scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(gsuite_auth_file, scopes)
                creds = flow.run_local_server(port=55042)
            # Save the credentials for the next run
            with open(file_token, 'w') as token:
                token.write(creds.to_json())

        # service = build('slides', 'v1', credentials=creds)
        # PRESENTATION_ID = "___"
        # # Call the Slides API
        # print('here')
        # gsheets = GSheets()
        #
        # body = {'properties': {'title': "AAAAAA sheet created from API" }}
        # result = gsheets.spreadsheets.create(body=body).execute()
        # pprint(result)
        # return
        # gslides = GSlides()
        # #pprint(gslides.all_presentations())
        # pprint(gslides.presentation_create("test from HBSec Bot"))
        # presentation = service.presentations().get(
        #     presentationId=PRESENTATION_ID).execute()
        # slides = presentation.get('slides')
        #
        # print('The presentation contains {} slides:'.format(len(slides)))
        # for i, slide in enumerate(slides):
        #     print('- Slide #{} contains {} elements.'.format(
        #         i + 1, len(slide.get('pageElements'))))


from oauth2client            import file, client
from oauth2client.tools      import argparser, run_flow

from osbot_aws.apis.Secrets  import Secrets
from osbot_utils.utils.Files import file_not_exists, file_contents, file_create


class GSuite_Setup():

    def __init__(self):
        self.secret_id_gsuite_client_secret = 'gwbot_gsuite_client_secret'
        self.secret_id_gsuite_token         = 'gwbot_gsuite_token'
        self.secret_id_with_credentials     = 'gsuite_token'
        self.secret_id_to_create            = 'gsuite_gsbot_user'
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

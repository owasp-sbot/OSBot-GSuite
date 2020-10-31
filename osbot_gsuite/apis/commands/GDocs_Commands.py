import base64

from osbot_aws.helpers.Lambda_Helpers import slack_message
from osbot_aws.apis.Secrets import Secrets

from osbot_gsuite import version_osbot_gsuite
from osbot_gsuite.apis.GDrive import GDrive
from osbot_gsuite.apis.GSlides import GSlides
from osbot_utils.utils.Files import Files


class GDocs_Commands:
    gsuite_secret_id = 'gwbot_gsuite_token_2' #'gsuite_gsbot_user'

    @staticmethod
    def _gdrive():
        return GDrive(GDocs_Commands.gsuite_secret_id)

    @staticmethod
    def _gslides():
        return GSlides(GDocs_Commands.gsuite_secret_id)

    # @staticmethod
    # def _resolve_secret_id(team_id):
    #     if team_id == 'T7F3AUXGV':    return 'slack-gs-bot'
    #     if team_id == 'T0SDK1RA8':    return 'slack-gsbot-for-pbx'

    def _send_pdf_to_slack(pdf_data, channel): #todo: refactor to separate method
        import requests
        aws_secrets_id  = 'slack-bot-oauth'
        bot_token       = Secrets(aws_secrets_id).value()
        tmp_file        = Files.temp_file('.pdf')
        with open(tmp_file, "wb") as fh:
            fh.write(base64.decodebytes(pdf_data.encode()))

        my_file = {
            'file': ('/tmp/file.pdf', open(tmp_file, 'rb'), 'pdf')
        }
        payload = {
            "filename": '{0}.png'.format('pdf'),
            "token": bot_token,
            "channels": [channel],
        }
        requests.post("https://slack.com/api/files.upload", params=payload, files=my_file)
        #return my_file

    # @staticmethod
    # def list(team_id, channel, params):
    #     folder_id       = '16yOkKyi0TfOy3w4IMW40vo-pr--Wa1Y9'
    #     link_template   = 'https://drive.google.com/open?id='
    #     files           = GDocs_Commands._gdrive().files_in_folder(folder_id)
    #     attachment_text = ""
    #     text            = ":point_right: Found {0} files in the current gsbot docs folder".format(len(files))
    #     for file in files:
    #         title   = file.get('name')
    #         file_id = file.get('id')
    #         url   = link_template + file_id
    #         attachment_text += " • <{0}|{1}> \n".format(url,title)
    #
    #     attachments = [{ 'color':'good', 'text': attachment_text}]
    #
    #     return text, attachments

    @staticmethod
    def pdf(team_id=None, channel=None, params=None):
        if params and len(params) > 0:
            file_id = params.pop()
            slack_message(":point_right: creating pdf for file: `{0}`".format(file_id), [], channel, team_id)
            pdf_bytes = GDocs_Commands._gdrive().file_export(file_id)
            pdf_data = base64.b64encode(pdf_bytes).decode()
            GDocs_Commands._send_pdf_to_slack(pdf_data, channel)
            # payload = {
            #     'pdf_data'      : pdf_data                                  ,
            #     'title'         : 'export_pdf'                              ,
            #     'aws_secrets_id': GDocs_Commands._resolve_secret_id(team_id),
            #     'channel'       : channel
            # }
            #return len(pdf_data)

            #Lambda('utils.pdf_to_slack').invoke(payload)

        return None,None

    @staticmethod
    def version(team_id=None, channel=None, params=None):
        return version_osbot_gsuite,[]
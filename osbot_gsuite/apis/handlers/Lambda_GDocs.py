from pbx_gs_python_utils.utils.Lambdas_Helpers              import log_to_elk
from pbx_gs_python_utils.utils.slack.Slack_Commands_Helper  import Slack_Commands_Helper
from osbot_gsuite.apis.commands.GDocs_Commands              import GDocs_Commands


class Lambda_GDocs:
    def handle_lambda_event(self, event):
        log_to_elk('[Lambda_GDocs]: {0}'.format(event))
        params  = event.get('params')
        data    = event.get('data')
        if data is not None:
            channel = data.get('channel')
            team_id = data.get('team_id')
            return Slack_Commands_Helper(GDocs_Commands).invoke(team_id, channel, params)
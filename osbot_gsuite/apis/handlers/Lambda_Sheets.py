from gw_bot.api.Slack_Commands_Helper import Slack_Commands_Helper
from osbot_gsuite.apis.commands.Sheets_Commands import Sheets_Commands


class Lambda_Sheets:
    def handle_lambda_event(self, event):

        params  = event.get('params')
        data    = event.get('data')
        if data:
            channel = data.get('channel')
            team_id = data.get('team_id')
            #log_to_elk('[Lambda_Slides]: {0}'.format(event))
            Slack_Commands_Helper(Sheets_Commands).invoke(team_id, channel, params)
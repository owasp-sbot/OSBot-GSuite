from gw_bot.api.Slack_Commands_Helper import Slack_Commands_Helper
from osbot_gsuite.apis.commands.Calendar_Commands import Calendar_Commands


class Lambda_Calendar:
    def handle_lambda_event(self, event):

        params  = event.get('params')
        data    = event.get('data')
        if data:
            channel = data.get('channel')
            team_id = data.get('team_id')
            return Slack_Commands_Helper(Calendar_Commands).invoke(team_id, channel, params)
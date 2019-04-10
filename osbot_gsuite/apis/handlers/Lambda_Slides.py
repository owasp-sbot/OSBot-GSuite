from osbot_gsuite.apis.commands.Slides_Commands            import Slides_Commands
from pbx_gs_python_utils.utils.slack.Slack_Commands_Helper import Slack_Commands_Helper


class Lambda_Slides:
    def handle_lambda_event(self, event):

        params  = event.get('params')
        data    = event.get('data')
        if data is not None:
            channel = data.get('channel')
            team_id = data.get('team_id')
            return Slack_Commands_Helper(Slides_Commands).invoke(team_id, channel, params)
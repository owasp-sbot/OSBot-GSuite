from osbot_gsuite.apis.GCalendar import GCalendar

class Calendar_Commands:
    gsuite_secret_id = 'gsuite_gsbot_user'

    @staticmethod
    def gs_team(team_id=None, channel=None, params=None):
        calendar = GCalendar(Calendar_Commands.gsuite_secret_id)
        return calendar.gs_team()
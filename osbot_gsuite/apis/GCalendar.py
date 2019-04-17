import datetime

from osbot_gsuite.apis.GSuite import GSuite


class GCalendar:

    def __init__(self, gsuite_secret_id=None):
        self.events = GSuite(gsuite_secret_id).calendar_v3().events()

    def _get_this_weeks_calendar_data(self, calendar_id):

        #now = datetime.datetime.utcnow().isoformat() + 'Z'
        time_min = '2019-03-17T00:00:00Z'
        time_max = '2019-03-23T00:00:00Z'

        events_result = self.events.list(calendarId = calendar_id,
                                         timeMin    = time_min,
                                         timeMax    = time_max,
                                         singleEvents=True,
                                         orderBy='startTime').execute()
        return events_result.get('items', [])

    def gs_team(self):
        calendar_id = 'photobox.com_kkecukq11iksaamp12p5mqdku0@group.calendar.google.com'
        return self._get_this_weeks_calendar_data(calendar_id)

    def gs_cs_team(self):
        calendar_id = 'photobox.com_b45nntbjhc2255c7dvf1l6ragc@group.calendar.google.com'
        return self._get_this_weeks_calendar_data(calendar_id)
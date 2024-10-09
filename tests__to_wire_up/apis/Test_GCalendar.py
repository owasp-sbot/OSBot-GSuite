from unittest import TestCase
from gsuite.GCalendar import GCalendar
from utils.Dev import Dev


class Test_GCalendar(TestCase):
    def setUp(self):
        self.gsuite_secret_id = 'gsuite_gsbot_user'
        self.calendar = GCalendar(self.gsuite_secret_id)


    def test_gs_team(self):
        events = self.calendar.gs_team()
        for event in events:
            Dev.pprint("{0} {1} - {2}".format(event.get('start'),event.get('end'),event.get('summary')))

    def test_gs_cs_team(self):
        events = self.calendar.gs_cs_team()
        for event in events:
            Dev.pprint("{0} {1} - {2}".format(event.get('start'),event.get('end'),event.get('summary')))
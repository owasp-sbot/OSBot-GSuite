from unittest import TestCase

from gs_budget.gsbot.Calendar_Commands import Calendar_Commands
from utils.Dev import Dev


class Test_Calendar_Commands(TestCase):

    def setUp(self):
        self.calendar = Calendar_Commands()

    def test_list_10(self):

        result = self.calendar.list_10()
        Dev.pprint(result)
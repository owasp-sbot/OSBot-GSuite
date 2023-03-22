from unittest import TestCase

from osbot_gsuite.analysis.Incident_Mass_Delete import Incident_Mass_Delete
from osbot_utils.utils.Dev import pprint


class test_Incident_Mass_Delete(TestCase):

    def setUp(self) -> None:
        self.incident_mass_delete = Incident_Mass_Delete()
        self.gdrive_activity      = self.incident_mass_delete.gdrive_activity

    def test_raw_activities(self):
        raw_activities = self.incident_mass_delete.raw_activities()
        pprint(len(raw_activities))

    def test_actions(self):
        max = 10
        actions = self.incident_mass_delete.actions(max=max)

        pprint(actions)
        #pprint(actions)

    def test_persons_details_from_actions(self):
        max = 1000
        actions = self.incident_mass_delete.actions(max=max)
        persons = self.gdrive_activity.persons_details_from_actions(actions)
        pprint(persons)

    def test_gsheet_data_from_actions(self):
        max = 10
        actions = self.incident_mass_delete.actions(max=max)
        result = self.incident_mass_delete.gsheet_data_from_actions(actions)
        pprint(result)

    def test_gsheet_send_actions_data(self):
        max = 100000
        file_id = '....'
        sheet_name = 'Activities - up to Mar 19'
        actions = self.incident_mass_delete.actions(max=max)
        result = self.incident_mass_delete.gsheet_send_actions_data(actions, file_id, sheet_name)
        pprint(result)
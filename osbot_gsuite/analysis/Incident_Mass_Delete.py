from osbot_gsuite.apis.GDrive_Activity import GDrive_Activity
from osbot_gsuite.apis.GSheet import GSheet
from osbot_gsuite.apis.GSheets import GSheets
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Json import json_load_file

TEMP_ACTIVITIES_PATH = '/tmp/gdrive_activity.json'


class Incident_Mass_Delete:

    def __init__(self):
        self.gdrive_activity = GDrive_Activity()
        return

    def raw_activities(self):
        return json_load_file(TEMP_ACTIVITIES_PATH)

    def actions(self, max=2):
        raw_activities = self.raw_activities()
        if max >0:
            raw_activities = raw_activities[:max]
        actions = self.gdrive_activity.parse_activities(raw_activities)
        self.resolve_actions_persons(actions)
        return actions

    def resolve_actions_persons(self, actions):
        persons = self.gdrive_activity.persons_details_from_actions(actions)
        for action in actions:
            person_id              = action.get('person_id')
            person                 = persons.get(person_id)
            action['display_name'] = person.get('display_name', 'unknown')

    def gsheet_data_from_actions(self, actions):
        rows = []
        for action in actions:
            target      = action.get('target'      )
            action_name = action.get('action_name' )
            action_data = action.get('action_data')
            target_data = action.get('target_data')
            row = {"Date"         : action.get('date'        ),
                   "Time"         : action.get('time'        ),
                   "Name"         : action.get('display_name'),
                   "Action"       : action_name               ,
                   #"action_data": action.get('action_data'),
                   "Target"       : target                    ,
                   'Target Title' : target_data.get('title'  ),
                   #"target_data": action.get('target_data'),
                   "Person_id"    : action.get('person_id'),
                   }

            rows.append(row)
        return rows

    def gsheet_send_actions_data(self, actions, file_id, sheet_name='Sheet1'):
        gsheets = GSheets()
        gsheet_data = self.gsheet_data_from_actions(actions)
        return gsheets.set_sheet_data(file_id, sheet_name, gsheet_data)

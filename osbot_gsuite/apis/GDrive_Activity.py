from dateutil import parser

from osbot_gsuite.apis.GDrive import GDrive
from osbot_gsuite.apis.GPeople import GPeople
from osbot_gsuite.apis.GSuite import GSuite
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.decorators.methods.cache_on_tmp import cache_on_tmp
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Json import json_save_file
from osbot_utils.utils.Misc import list_set
from osbot_utils.utils.Python_Logger import logger_info

TEMP_ACTIVITIES_PATH = '/tmp/gdrive_activity.json'

class GDrive_Activity:

    def __init__(self):
        self.log_info = logger_info()
        self.gpeople = GPeople()

    @cache_on_self
    def activity(self):
        return GSuite().drive_activity_v2().activity()

    def gdrive(self):
        return GDrive()

    #@cache_on_tmp()
    def query(self, item=None, page_size=2, recursive=False, loop=1):
        body           = { 'pageSize': page_size ,
                           'pageToken': None}
        request_params = { 'body'    : body      }
        if item:
            if recursive:
                body['ancestorName'] = f'items/{item}'
            else:
                body['itemName'] = f'items/{item}'

        all_activities = []
        for i in range(loop):
            self.log_info(f"making request #{i+1} of {loop}")
            result = self.activity().query(**request_params).execute()
            activities      = result.get('activities', [])
            next_page_token = result.get('nextPageToken')
            self.log_info(f"got {len(activities)} activities")
            all_activities.extend(activities)
            if next_page_token is None:
                break
            body['pageToken'] = next_page_token
        self.save_all_activities(all_activities)
        #return activities
        return self.parse_activities(all_activities)

    def parse_activity(self, activity):
        actions               = activity.get('actions')
        actors                = activity.get('actors')
        primary_action_detail = activity.get('primaryActionDetail')
        targets               = activity.get('targets')
        time_stamp            = activity.get('timestamp')


        # assert expectations of data analysis below
        assert list_set(activity) == ['actions', 'actors', 'primaryActionDetail', 'targets', 'timestamp']
        assert len(actors) == 1

        actor       = actors.pop()
        user        = actor.get('user')
        known_user  = user.get('knownUser')
        person_name = known_user.get('personName')

        assert list_set(actor     ) == ['user'      ]
        assert list_set(user      ) == ['knownUser' ]
        assert list_set(known_user) == ['personName']
        assert len(person_name.split('/')) == 2
        assert len(targets)                == 1

        targets    = targets.pop()                              # since target has name value pairs inside it, and we have already asserted that it is only one value (via the assert above)
        person_id  = person_name.split('/').pop()
        date_time  = parser.parse(timestr=time_stamp)
        date       = str(date_time.date())
        time       = f'{date_time.hour}:{date_time.minute}.{date_time.second}'
        activities = []

        for action in actions:
            assert list_set(action) == ['detail']
            for action_name,action_data in action.get('detail').items():
                for target, target_data in targets.items():
                    activity = {'date'        : date        ,
                                'time'        : time        ,
                                'person_id'   : person_id   ,
                                'action_name' : action_name ,
                                'action_data' : action_data ,
                                'target'      : target      ,
                                'target_data' : target_data }
            activities.append(activity)
        return activities

    def parse_activities(self, activities):
        self.log_info(f'parsing {len(activities)} activities')
        actions = []
        for activity in activities:
            actions.extend(self.parse_activity(activity))
        self.log_info(f'which were expanded into {len(actions)} actions')
        return actions
        #return [self.parse_activity(activity for activity in activities)]

    def persons_details_from_actions(self, actions):
        persons = {}
        for action in actions:
            person_id = action.get('person_id')
            if person_id not in persons:
                persons[person_id] = {}

        self.log_info(f"There are {len(persons)} persons to resolve")
        for person_id in persons:
            try:
                persons[person_id] = self.gpeople.person(person_id)
            except Exception as error:
                self.log_info(f"Error resolving person id: {person_id} - {error}")
                persons[person_id] = { }
        return persons

    def save_all_activities(self, activities):
        result = json_save_file(activities, TEMP_ACTIVITIES_PATH, pretty=False)
        self.log_info(f'saved {len(activities)} activities to {TEMP_ACTIVITIES_PATH}')
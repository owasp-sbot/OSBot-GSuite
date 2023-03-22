from unittest import TestCase

from osbot_gsuite.apis.GDrive_Activity import GDrive_Activity
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import list_set


class test_GDrive_Activity(TestCase):

    def setUp(self):
        self.gdrive_activity = GDrive_Activity()

    def test_query(self):
        filter = "targets.driveItem.itemId='...'"
        filter = None
        item = '....'
        recursive=True
        page_size = 300
        loop = 20
        #item = None
        activities = self.gdrive_activity.query(page_size=page_size, filter=filter, item=item, recursive=recursive, loop=loop)
        #pprint(activities)

    def test_gdrive(self):
        result = self.gdrive_activity.gdrive().files_all(10)
        pprint(result)
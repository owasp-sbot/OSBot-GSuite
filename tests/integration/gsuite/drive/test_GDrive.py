from unittest import TestCase

from googleapiclient.discovery import Resource
from osbot_utils.utils.Misc import list_set

from osbot_utils.utils.Dev import pprint

from osbot_utils.utils.Env              import load_dotenv
from osbot_gsuite.gsuite.drive.GDrive   import GDrive


class test_GDrive(TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.gdrive = GDrive()

    def test_drive_v3__files__permissions(self):
        with self.gdrive as _:
            assert type(_.drive_v3   ()) is Resource
            assert type(_.files      ()) is Resource
            assert type(_.permissions()) is Resource

    def test_files_all(self):
        with self.gdrive as _:
            filed_names = sorted(["id", "name", "hasThumbnail", "kind", "mimeType", "modifiedTime", "webViewLink"])
            fields      = f"files({','.join(filed_names)})"
            files       = _.files_all(size=3, fields=fields)
            assert len(files) == 3
            for file in files:
                assert list_set(file) == filed_names


from unittest import TestCase

from osbot_gsuite.testing.OSBot__GSuite__Testing import ENV_NAME__GDRIVE__TEMP_FOLDER
from osbot_utils.utils.Env import load_dotenv, get_env
from osbot_utils.utils.Dev                          import pprint
from osbot_gsuite.gsuite.drive.Temp__GDrive__Folder import Temp__GDrive__Folder


class test_Temp_GDrive_Folder(TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.temp_gdrive_folder = Temp__GDrive__Folder()

    def test_parent_folder(self):
        assert self.temp_gdrive_folder.parent_folder() == get_env(ENV_NAME__GDRIVE__TEMP_FOLDER)

    # def test__enter__exit__(self):
    #     temp_folder_name = '__osbot_gsuite_temp_folder/sub-folder'
    #     with self.temp_gdrive_folder.gdrive as _:
    #         pprint(_.folders_list())
    #         #result = _.folder_create(temp_folder_name)
    #         #folder_id =
    #         #pprint(result)
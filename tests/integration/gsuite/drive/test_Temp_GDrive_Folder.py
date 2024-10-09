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
    #     parent_folder = self.temp_gdrive_folder.parent_folder()
    #     temp_folder_name = 'an_temp_folder'
    #     with self.temp_gdrive_folder.gdrive as _:
    #         #temp_folder_id = _.folder_create(folder_name=temp_folder_name, parent_folder=parent_folder)
    #         temp_folder_id = '13u8FGbfQauaXM5M60UXojS56LpiOBKHG'
    #         pprint(temp_folder_id)
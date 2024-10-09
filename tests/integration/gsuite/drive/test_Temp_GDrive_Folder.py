from unittest                                       import TestCase
from osbot_gsuite.testing.OSBot__GSuite__Testing    import ENV_NAME__GDRIVE__TEMP_FOLDER
from osbot_utils.utils.Env                          import load_dotenv, get_env
from osbot_gsuite.gsuite.drive.Temp__GDrive__Folder import Temp__GDrive__Folder


class test_Temp__GDrive__Folder(TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.temp_gdrive_folder = Temp__GDrive__Folder()

    def test_parent_folder(self):
        assert self.temp_gdrive_folder.parent_folder() == get_env(ENV_NAME__GDRIVE__TEMP_FOLDER)

    def test__enter__exit__(self):
        with self.temp_gdrive_folder as _:
            folder_info = _.folder_info()
            assert _.folder_exists()                                          is True
            assert folder_info.id                                             == _.folder_id
            assert folder_info.kind                                           == "drive#file"
            assert folder_info.name                                           == _.folder_name
            assert folder_info.mimeType                                       == 'application/vnd.google-apps.folder'
            assert folder_info.name.startswith('osbot-gsuite-random-folder_') is True
            assert folder_info.parents                                        == [self.temp_gdrive_folder.parent_folder()]
            assert folder_info.webViewLink                                    == f'https://drive.google.com/drive/folders/{_.folder_id}'

        assert _.folder_exists() is False
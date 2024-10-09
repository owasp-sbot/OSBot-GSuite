from unittest import TestCase

from osbot_gsuite.apis.utils.GDrive_Folder import GDrive_Folder
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_not_exists, file_name
from osbot_utils.utils.Http import GET_bytes_to_file
from osbot_utils.utils.Misc import wait_for


class test_GDrive_Folder(TestCase):

    def setUp(self) -> None:
        self.url_test_file   = 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png'
        self.local_test_file = '/tmp/upload_test_file.png'
        folder_name = 'Bot_Files'
        folder_id   = '1s3p0y4WUlq8SLyeSyx7WN4nwJitAjX3z'
        self.gdrive_folder = GDrive_Folder(folder_name=folder_name, folder_id=folder_id)
        if file_not_exists(self.local_test_file):
            GET_bytes_to_file(url=self.url_test_file, path=self.local_test_file)


    def test_file_delete(self):
        file_id = '1C7PvqIJyHFef0ilQ3aE_omvjiyr1RdMl'
        result = self.gdrive_folder.file_delete(file_id)
        pprint(result)

    def test_file_info(self):
        file_id = '1C7PvqIJyHFef0ilQ3aE_omvjiyr1RdMl'
        result = self.gdrive_folder.file_info(file_id)
        pprint(result)


    def test_upload_file(self):
        self.gdrive_folder.folder_create()
        file_id   = self.gdrive_folder.file_upload_png(self.local_test_file)
        file_info = self.gdrive_folder.file_info(file_id)
        assert file_info.get('name') == file_name(self.local_test_file)
        self.gdrive_folder.file_delete(file_id)
        assert self.gdrive_folder.file_info(file_id) is None

    def test_files(self):
        result = self.gdrive_folder.files()
        pprint(result)

    def test_image_url(self):
        image_id = self.gdrive_folder.file_upload_png(self.local_test_file)
        image_url = "https://lh3.google.com/u/1/d/{0}".format(image_id)
        print(image_url)

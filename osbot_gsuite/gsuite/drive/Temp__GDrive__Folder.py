from osbot_utils.utils.Misc import random_text

from osbot_gsuite.gsuite.drive.GDrive               import GDrive
from osbot_gsuite.testing.OSBot__GSuite__Testing    import osbot_gsuite_testing
from osbot_utils.base_classes.Type_Safe             import Type_Safe


class Temp__GDrive__Folder(Type_Safe):
    gdrive      : GDrive
    folder_id   : str
    folder_name : str = random_text('osbot-gsuite-random-folder')

    def parent_folder(self):
        return osbot_gsuite_testing.gdrive_temp_folder()

    def __enter__(self):
        self.folder_create()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.folder_delete()

    def folder_create(self):
        kwargs = dict(folder_name   = self.folder_name    ,
                      parent_folder = self.parent_folder())
        self.folder_id = self.gdrive.folder_create(**kwargs)
        return self.folder_id

    def folder_delete(self):
        return self.gdrive.folder_delete(self.folder_id)

    def folder_exists(self):
        return self.gdrive.folder_exists(self.folder_id)

    def folder_info(self):
        return self.gdrive.folder_info(self.folder_id)
from osbot_gsuite.gsuite.drive.GDrive import GDrive
from osbot_gsuite.testing.OSBot__GSuite__Testing import osbot_gsuite_testing
from osbot_utils.base_classes.Type_Safe import Type_Safe


class Temp__GDrive__Folder(Type_Safe):
    gdrive: GDrive

    def parent_folder(self):
        return osbot_gsuite_testing.gdrive_temp_folder()

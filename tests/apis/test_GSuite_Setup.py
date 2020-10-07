import json
import os
from distutils.dir_util import copy_tree
from unittest import TestCase
from osbot_aws.apis.Secrets import Secrets
from osbot_gsuite.apis.GDrive import GDrive
from osbot_gsuite.apis.GSheets import GSheets
from osbot_gsuite.apis.GSuite_Setup import GSuite_Setup
from osbot_utils.utils.Dev import Dev
from osbot_utils.utils.Files import file_contents


class test_GSuite_Setup(TestCase):

    def setUp(self):
        self.gsuite_setup = GSuite_Setup()
        self.filename_with_gsuite_client_secret = 'client_secret_538397666918-ftcpk1s9u8gbgmc47c7ocb9kdll4m7j3.apps.googleusercontent.com.json'
        self.file_with_credentials              = f'{os.getenv("HOME")}/Downloads/{self.filename_with_gsuite_client_secret}'
        self.scopes                             = [ 'https://www.googleapis.com/auth/calendar'       ,
                                                    'https://www.googleapis.com/auth/documents'      ,
                                                    'https://www.googleapis.com/auth/drive'          ,
                                                    'https://www.googleapis.com/auth/presentations'  ,
                                                    'https://www.googleapis.com/auth/spreadsheets'   ]


    def test_save_gsuite_client_secret_in_aws(self):
        self.gsuite_setup.save_gsuite_client_secret_in_aws(self.file_with_credentials)

    def test_create_auth_token_using_web_browser_flow(self):
        self.gsuite_setup.create_auth_token_using_web_browser_flow(self.scopes)

    def test_check_secret_works(self):
        os.environ['AWS_REGION'] = 'london'  # simulate AWS environment
        gdrive = GDrive(self.gsuite_setup.secret_id_gsuite_token)
        files = gdrive.files_all(10)
        Dev.pprint(files)
        #GSheets(self.gsuite_setup.secret_id_gsuite_token)
        #assert len(GSheets(self.gsuite_setup.secret_id_gsuite_token).all_spreadsheets()) > 0



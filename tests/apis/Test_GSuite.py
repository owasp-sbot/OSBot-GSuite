from unittest       import TestCase

from osbot_aws.apis.Secrets import Secrets
from osbot_gsuite.apis.GSuite import GSuite
from osbot_utils.utils.Dev import Dev
from osbot_utils.utils.Files import file_contents
from osbot_utils.utils.Json import Json


class Test_GSuite(TestCase):
    def setUp(self):
        self.gsuite = GSuite()

    def test__init__(self):
        self.gsuite.gsuite_secret_id == 'gsuite_token'

    def test_get_oauth_token_drive(self):
        token_file = self.gsuite.get_oauth_token('drive.metadata.readonly')
        token_values = Json.load_file(token_file)
        assert token_values['scopes'] == ['https://www.googleapis.com/auth/drive.metadata.readonly']

    def test_get_oauth_token_admin(self):
        token_file = self.gsuite.get_oauth_token('admin.reports.audit.readonly')
        token_values = Json.load_file(token_file)
        assert token_values['scopes'] == ['https://www.googleapis.com/auth/admin.reports.audit.readonly']

    # install json token in secret
    def test_create_aws_secret_with_json_token_in(self):
        import os


    def test_create_oauth_token(self):
        gsuite    = GSuite()
        gsuite.get_oauth_creds('drive')




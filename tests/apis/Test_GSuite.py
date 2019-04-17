from unittest       import TestCase
from gsuite.GSuite  import GSuite
from utils.Json import Json


class Test_GSuite(TestCase):
    def setUp(self):
        self.gsuite = GSuite()

    def test__init__(self):
        self.gsuite.gsuite_secret_id == 'gsuite_token'

    def test_get_oauth_token_drive(self):
        token_file = self.gsuite.get_oauth_token('drive.metadata.readonly')
        token_values = Json.load_json(token_file)
        assert token_values['scopes'] == ['https://www.googleapis.com/auth/drive.metadata.readonly']

    def test_get_oauth_token_admin(self):
        token_file = self.gsuite.get_oauth_token('admin.reports.audit.readonly')
        token_values = Json.load_json(token_file)
        assert token_values['scopes'] == ['https://www.googleapis.com/auth/admin.reports.audit.readonly']



    #def test_admin_reports(self):
    #    result = self.gsuite.admin_reports_v1()
    #    Dev.pprint(result)

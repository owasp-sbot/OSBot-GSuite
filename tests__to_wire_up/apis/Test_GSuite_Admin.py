from unittest             import TestCase
from gsuite.GSuite_Admin  import GSuite_Admin
from utils.Dev            import Dev


class Test_GSuite_Admin(TestCase):
    def setUp(self):
        self.gsuite_admin = GSuite_Admin()

    def test_ctor(self):
        service = self.gsuite_admin.service
        assert service._baseUrl == 'https://www.googleapis.com/admin/reports/v1/'

    def test_get_api_data(self):
        login_data = self.gsuite_admin.get_api_data('login',100)
        assert len(login_data) == 100
        assert login_data.pop().get('id').get('applicationName') == 'login'

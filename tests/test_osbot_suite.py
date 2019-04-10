import sys; sys.path.append('..')
from unittest import TestCase
import osbot_gsuite


class test_gsbot_suite(TestCase):

    def test__init__(self):
        assert type(osbot_gsuite.version_osbot_gsuite) is str


    def test_CHECK_FILE_ACCESS(self):
        from osbot_gsuite.apis.GSheets import GSheets
        from pbx_gs_python_utils.utils.Dev import Dev

        file_id = '1Zwzn1zc5xukhC9Sn1elWwXfHIIMghnXZHw0iOLy2x9s'

        result = GSheets().sheets_metadata(file_id)

        Dev.pprint(result)

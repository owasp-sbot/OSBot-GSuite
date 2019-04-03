from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev


from pbx_gs_python_utils.utils.Dev             import Dev
from pbx_gs_python_utils.utils.Files           import Files
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message

class Test_qa_environment:

    def test_console_test(self):
        Dev.pprint('it is working')
        Dev.pprint(Files.exists('../../libs/pbx-gs-python-utils/pbx_gs_python_utils'))

    def test_assert_test(self):
        assert 1==1

    def test_send_slack_message(self):
        slack_message('this is a test from `test_Simple_Test`')

class test_Simple_Test(TestCase):

    def test_an_example(self):
        Dev.pprint("**** This is my first test....")


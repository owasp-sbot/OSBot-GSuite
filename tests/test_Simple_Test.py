from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev


class test_Simple_Test(TestCase):

    def test_an_example(self):
        Dev.pprint("**** This is my first test....")
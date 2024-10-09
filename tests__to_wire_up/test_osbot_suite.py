import sys; sys.path.append('..')
from unittest import TestCase
import osbot_gsuite


class test_gsbot_suite(TestCase):

    def test__init__(self):
        assert type(osbot_gsuite.version_osbot_gsuite) is str

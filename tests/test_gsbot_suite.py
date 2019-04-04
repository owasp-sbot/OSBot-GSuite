import sys; sys.path.append('..')
from unittest import TestCase
import gsbot_gsuite


class test_gsbot_suite(TestCase):

    def test__init__(self):
        assert type(gsbot_gsuite.version_gsbot_gsuite) is str
from unittest import TestCase

from osbot_gsuite.apis.GPeople import GPeople
from osbot_utils.utils.Dev import pprint


class test_GPeople(TestCase):

    def setUp(self):
        self.gpeople = GPeople()

    def test_person_raw(self):

        person_id = '....'
        person_fields = 'all'
        #person_fields = None
        person_raw = self.gpeople.person_raw(person_id, person_fields)

        pprint(person_raw)

    def test_person(self):

        person_id = '....'

        info = self.gpeople.person(person_id)

        pprint(info)
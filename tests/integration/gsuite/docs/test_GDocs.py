from unittest import TestCase

from googleapiclient.discovery import Resource
from osbot_utils.utils.Misc import random_text

from osbot_utils.utils.Dev import pprint

from osbot_gsuite.testing.OSBot__GSuite__Testing import osbot_gsuite_testing
from osbot_utils.utils.Env import load_dotenv

from osbot_gsuite.gsuite.docs.GDocs import GDocs


class test_GDocs(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_folder_id = osbot_gsuite_testing.gdrive_temp_folder()
        cls.gdocs          = GDocs()

    def test_setUpClass(self):
        with self.gdocs as _:
            assert type(_) is GDocs
            assert type(_.docs_v1  ()) is Resource
            assert type(_.documents()) is Resource

    def test_document_create(self):
        with self.gdocs as _:
            temp_title = random_text('an temp title')
            result     = _.document_create(title=temp_title, folder_id=self.temp_folder_id)
            doc_id     = result.doc_id
            doc_info   = result.doc_info
            assert doc_info.title            == temp_title
            assert doc_info.documentId       == doc_id
            assert _.document_delete(doc_id) is True



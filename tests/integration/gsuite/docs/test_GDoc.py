from unittest import TestCase

from osbot_utils.utils.Dev import pprint

from osbot_gsuite.gsuite.docs.GDoc              import GDoc
from osbot_gsuite.gsuite.docs.Temp__GDocs__File import Temp__GDocs__File


class test_GDoc(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_gdocs_file = Temp__GDocs__File()
        cls.temp_gdocs_file.file_create()
        cls.gdoc = GDoc(file_id=cls.temp_gdocs_file.doc_id)

    @classmethod
    def tearDownClass(cls):
        cls.temp_gdocs_file.file_delete()

    def test_info(self):
        with self.gdoc as _:
            assert _.info() == { '# requests committed' : 0                            ,
                                 '# requests queued'    : 0                            ,
                                 'file_id'              : self.temp_gdocs_file.doc_id  ,
                                 'file_name'            : self.temp_gdocs_file.title   }

    def test_body(self):
        with self.gdoc as _:
            assert len(_.body().content) == 2

    def test_pdf__bytes(self):
        with self.gdoc as _:
            assert _.pdf__bytes().startswith(b'%PDF-1.4\n%\xd3\xeb\xe9\xe1')


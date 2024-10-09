from unittest import TestCase

from googleapiclient.discovery import Resource
from osbot_utils.utils.Files import file_not_exists, file_exists, file_bytes, file_copy

from osbot_utils.testing.Temp_File import Temp_File

from osbot_gsuite.gsuite.slides.Temp__GSlides__Presentation import Temp__GSlides__Presentation
from osbot_utils.utils.Misc import random_text

from osbot_utils.utils.Dev import pprint

from osbot_gsuite.gsuite.slides.GSlides import GSlides
from osbot_gsuite.testing.OSBot__GSuite__Testing import osbot_gsuite_testing


class test_GSlides(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_presentation = Temp__GSlides__Presentation()
        cls.temp_presentation.presentation_create()
        cls.gslides        = GSlides()

    @classmethod
    def tearDownClass(cls):
        cls.temp_presentation.presentation_delete()


    def test_setUpClass(self):
        with self.gslides as _:
            assert type(_) is GSlides
            assert type(_.slides_v1    ()) is Resource
            assert type(_.presentations()) is Resource

    def test_all_presentations(self):
        with self.gslides as _:
            presentations = _.all_presentations()               # todo: add mode to only get 5 presentations 
            assert len(presentations) > 0

    def test_pdf__bytes(self):
        with self.gslides as _:
            pdf_bytes = _.pdf__bytes(self.temp_presentation.presentation_id)
            assert pdf_bytes[0:8] == b'%PDF-1.4'

    def test_pdf__file(self):
        with Temp_File(extension='.pdf', create_file=False) as temp_file:
            pdf_file        = temp_file.file_path
            presentation_id   = self.temp_presentation.presentation_id
            presentation_info = self.temp_presentation.presentation_data.presentation_info
            page_id           = presentation_info.slides[0].objectId
            with self.gslides as _:

                # pprint(page_id)
                # result = _.element_create_text(presentation_id, page_id, 'Hello World', 100, 100)
                # pprint(result)

                assert file_not_exists(pdf_file)
                assert _.pdf__file(self.temp_presentation.presentation_id, pdf_file) == pdf_file
                assert file_exists(pdf_file)
                assert file_bytes(pdf_file)[0:8] == b'%PDF-1.4'

class test_GSlides_2(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.gslides = GSlides()

    def test_element_create_text(self):
        with self.gslides as _:
            title             = random_text('osbot-gsuite-random-presentation')
            folder_id         = osbot_gsuite_testing.gdrive_temp_folder()
            presentation_data = _.presentation_create(title, folder_id)
            presentation_id   = presentation_data.presentation_id
            presentation_info = presentation_data.presentation_info

            text_1 = 'And the answer is|||||||'
            text_2 = '... always 42'
            object_id_1 = presentation_info.slides[0].pageElements[0].objectId
            object_id_2 = presentation_info.slides[0].pageElements[1].objectId
            _.element_set_text(presentation_id, object_id_1, text_1, delete_existing_text=False)
            _.element_set_text(presentation_id, object_id_2, text_2, delete_existing_text=False)

            #_.pdf__file(presentation_id, './an_presentations.pdf')
            _.presentation_delete(presentation_id)


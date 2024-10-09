from unittest                                       import TestCase

from osbot_gsuite.gsuite.slides.Temp__GSlides__Presentation import Temp__GSlides__Presentation
from osbot_utils.utils.Misc import wait_for

from osbot_utils.utils.Dev import pprint

from osbot_gsuite.gsuite.docs.Temp__GDocs__File import Temp__GDocs__File
from osbot_gsuite.testing.OSBot__GSuite__Testing    import ENV_NAME__GDRIVE__TEMP_FOLDER
from osbot_utils.utils.Env                          import load_dotenv, get_env



class test_Temp__GSlides__Presentation(TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.temp_slides_presentation = Temp__GSlides__Presentation()

    def test_parent_folder(self):
        assert self.temp_slides_presentation.parent_folder() == get_env(ENV_NAME__GDRIVE__TEMP_FOLDER)

    def test__enter__exit__(self):
        with self.temp_slides_presentation as _:
            presentation_info = _.presentation_info()
            assert _.presentation_exists()           is True
            assert presentation_info.title           == _.title
            assert presentation_info.presentationId  == _.presentation_id

        # todo: see if there is a better way to do this, since there we were times (in CI Pipeline) where it took more than 4 seconds to delete the file
        #       and I know othe file is being deleted since it shows for a couple secs in temp folder (and then is deleted)
        #assert _.file_exists() is False                        # BUG: this is failing (the file is not being deleted immediately)
        # for i in range(20):                                     # interesting race condition here where the file can take a few seconds to be deleted
        #     result = _.file_exists()
        #     if result is False:
        #         break
        #     wait_for(0.2)                                       # it can take up to 4 secs
        #
        # assert _.file_exists() is False                         # now we can confirm that the file has been deleted

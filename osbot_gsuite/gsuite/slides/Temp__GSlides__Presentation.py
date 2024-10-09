from types                                          import SimpleNamespace
from osbot_gsuite.gsuite.slides.GSlides             import GSlides
from osbot_utils.utils.Misc                         import random_text
from osbot_gsuite.testing.OSBot__GSuite__Testing    import osbot_gsuite_testing
from osbot_utils.base_classes.Type_Safe             import Type_Safe


class Temp__GSlides__Presentation(Type_Safe):
    gslides           : GSlides
    title             : str = random_text('osbot-gsuite-random-presentation')
    presentation_data : SimpleNamespace
    presentation_id   : str

    def parent_folder(self):
        return osbot_gsuite_testing.gdrive_temp_folder()

    def __enter__(self):
        self.presentation_create()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.presentation_delete()

    def presentation_create(self):
        kwargs = dict(title   = self.title    ,
                      folder_id = self.parent_folder())
        self.presentation_data = self.gslides.presentation_create(**kwargs)
        self.presentation_id   = self.presentation_data.presentation_id
        return self.presentation_id

    def presentation_delete(self):
        return self.gslides.presentation_delete(self.presentation_id)

    def presentation_exists(self):
        return self.gslides.presentation_exists(self.presentation_id)

    def presentation_info(self):
        return self.gslides.presentation_metadata(self.presentation_id)
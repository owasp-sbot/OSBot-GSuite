from unittest import TestCase

from osbot_gsuite.gsuite.slides.GSlides import GSlides


class test_GSlides(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.gslides = GSlides()



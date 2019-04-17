from unittest import TestCase

from utils.Dev import Dev
from utils.aws.Lambdas import Lambdas


class Test_Lambda_lambda_calendar(TestCase):
    def setUp(self):
        self.lambda_graph = Lambdas('gs.lambda_calendar', memory=3008).delete()

    def test_update(self):
        self.lambda_graph.update_with_src()

    def test_update_invoke(self):
        result = self.lambda_graph.update_with_src().invoke({ 'data': {'a':123}, "params": ["gs_team"]})
        Dev.pprint(result)

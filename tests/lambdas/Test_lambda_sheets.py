from unittest import TestCase

from osbot_aws.apis.Lambda import Lambda
from osbot_utils.utils.Dev import Dev

from osbot_gsuite.lambdas.sheets import run


class Test_Lambda_lambda_sheets(TestCase):
    def setUp(self):
        self.lambda_graph = Lambda('osbot_gsuite.lambdas.sheets')

    def test_invoke_directly(self):
        result = run({},{})
        Dev.pprint(result)

    def test_update_invoke(self):
        result = self.lambda_graph.invoke({ 'data': {}})
        Dev.ppring(result.print())
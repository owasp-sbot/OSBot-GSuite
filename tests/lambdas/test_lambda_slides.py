from unittest import TestCase

from pbx_gs_python_utils.lambdas.gs.lambda_slides import run
from pbx_gs_python_utils.utils.aws.Lambdas import Lambdas


class Test_Lambda_lambda_slides(TestCase):
    def setUp(self):
        self.lambda_graph = Lambdas('pbx_gs_python_utils.lambdas.gs.lambda_slides', memory=3008).create()

    # def test_update(self):
    #     self.lambda_graph.update_with_lib()

    def test_invoke_directly(self):
        assert run({ 'data':{}},{})[0] == '*Here are the `Slides_Commands` commands available:*'

    def test_lambda_invoke(self):
        assert self.lambda_graph.invoke({ 'data': {}})[0] == '*Here are the `Slides_Commands` commands available:*'

    def test_version(self):
        assert self.lambda_graph.invoke({'data': {},'params':['version']})[0] == 'v0.22'

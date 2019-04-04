import unittest
from unittest import TestCase
from pbx_gs_python_utils.utils.aws.Lambdas  import Lambdas

from gsbot_gsuite import version_gsbot_gsuite
from gsbot_gsuite.lambdas.slides import run


class Test_Lambda_lambda_slides(TestCase):
    def setUp(self):
        self.lambda_graph = Lambdas('gsbot_gsuite.lambdas.slides', memory=3008)
        #path = Files.path_combine('.','../..')
        #self.lambda_graph.update_with_src(path)

    # def test_update(self):
    #     self.lambda_graph.update_with_lib()

    @unittest.skip('needs gmail dependency and s3 permissions are not defined')
    def test_invoke_directly(self):
        assert run({ 'data':{}},{})[0] == '*Here are the `Slides_Commands` commands available:*'

    def test_lambda_invoke(self):
        assert self.lambda_graph.invoke({ 'data': {}})[0] == '*Here are the `Slides_Commands` commands available:*'

    def test_version(self):
        assert 'v0.' in self.lambda_graph.invoke({'data': {},'params':['version']})[0]

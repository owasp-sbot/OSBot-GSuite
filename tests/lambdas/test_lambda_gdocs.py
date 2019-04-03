import unittest
from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Files import Files
from pbx_gs_python_utils.utils.aws.Lambdas import Lambdas

import gsbot_gsuite
from gsbot_gsuite.lambdas.gdocs import run


class test_Lambda_lambda_gdocs(TestCase):
    def setUp(self):
        self.lambda_gdocs = Lambdas('gsbot_gsuite.lambdas.gdocs', memory=3008)

        #path = Files.path_combine('.','../..')
        #self.lambda_gdocs.update_with_src(path)

    @unittest.skip('needs gmail dependency and s3 permissions are not defined')
    def test_invoke_directly(self):
        response = run({ 'data':{}},{})
        assert response[0] == '*Here are the `GDocs_Commands` commands available:*'

    def test_invoke___with_no_command(self):
        result = self.lambda_gdocs.invoke({'data': {}, 'params': []})
        assert result[0] == '*Here are the `GDocs_Commands` commands available:*'

    def test_pdf(self):
        result = self.lambda_gdocs.invoke({ 'data':{}, 'params':['pdf','1xIeV2eQb59EsiJoOUB1yOK3FY2LCvzMmTgvhAVXlEEI']})
        assert result == [None,None]

    def test_version(self):
        result = self.lambda_gdocs.invoke({'data': {}, 'params': ['version']})
        assert result == ['v0.22',[]]

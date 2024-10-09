from gw_bot.Deploy import Deploy
from osbot_aws.helpers.Test_Helper import Test_Helper
from osbot_aws.apis.Lambda import Lambda

from osbot_gsuite.lambdas.gdocs import run


class test_Lambda_lambda_gdocs(Test_Helper):
    def setUp(self):
        super().setUp()
        self.lambda_name = 'osbot_gsuite.lambdas.gdocs'
        self.lambda_gdocs = Lambda(self.lambda_name)

    def test_update(self):
        Deploy().deploy_lambda__gsuite(self.lambda_name)

    #@unittest.skip('to debug: was failing in CodeBuild')
    def test_invoke_directly(self):
        self.result = run({ 'data':{}},{})
        assert self.result[0] == '*Here are the `GDocs_Commands` commands available:*'

    def test_invoke__directly_pdf(self):
        file_id = '1j7gNbN4o4kO1Q_Qp39LC1AO_d23BrFZZHoutEkfz41I'
        self.result = run({'data': {'channel':'DRE51D4EM'}, 'params': ['pdf', file_id] }, {})

    def test_invoke___with_no_command(self):
        result = self.lambda_gdocs.invoke({'data': {}, 'params': []})
        assert result[0] == '*Here are the `GDocs_Commands` commands available:*'




    def test_pdf(self):
        self.test_update()
        file_id = '1j7gNbN4o4kO1Q_Qp39LC1AO_d23BrFZZHoutEkfz41I'
        result = self.lambda_gdocs.invoke({ 'data':{}, 'params':['pdf',file_id]})
        assert result == [None,None]

    def test_version(self):
        result = self.lambda_gdocs.invoke({'data': {}, 'params': ['version']})
        print()
        print(result)
        assert 'v0.' in result[0]

import sys ; sys.path.append('..')

from unittest import TestCase

from gsbot_gsuite.apis.commands.GDocs_Commands import GDocs_Commands

class test_GDocs_Commands(TestCase):

    # def test_update_lambda(self):
    #     Lambdas('gs.lambda_gdocs').update_with_src()

    def test_list(self):
        params = []
        text,attachments = GDocs_Commands.list(None, None, params)
        assert ":point_right: Found" in text

    def test_pdf(self):
        params = ["1xIeV2eQb59EsiJoOUB1yOK3FY2LCvzMmTgvhAVXlEEI"]
        team_id = 'T7F3AUXGV'
        channel = 'GDL2EC3EE'
        assert GDocs_Commands.pdf(team_id, channel,params) == (None, None)

    def test_pdf___no_value_provided(self):
        params = []
        assert GDocs_Commands.pdf(params=params) == (None, None)
import unittest
from unittest import TestCase

from osbot_aws.helpers.Lambda_Helpers import slack_message
from osbot_utils.utils.Dev import Dev

from gw_bot.Deploy import Deploy


class test_Deploy_Lambda_Functions(TestCase):

    def test_deploy_lambda_functions(self):
        targets = [
                    'osbot_gsuite.lambdas.gdocs'    ,   #   gdocs.py    Lambda_GDocs    GDocs_Commands
                    'osbot_gsuite.lambdas.slides'   ,   #   slides.py   Lambda_Slides   Slides_Commands

                   ]
        result = ""
        for target in targets:
            Deploy(target).deploy()
            result += " • {0}\n".format(target)

        text        = ":hotsprings: [osbot-gsuite] updated lambda functions"
        attachments = [{'text': result, 'color': 'good'}]
        slack_message(text, attachments)  # gs-bot-tests
        Dev.pprint(text, attachments)


if __name__ == '__main__':
    unittest.main()
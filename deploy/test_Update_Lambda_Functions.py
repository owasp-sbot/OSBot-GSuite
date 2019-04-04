import unittest
from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Files import Files
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message
from pbx_gs_python_utils.utils.aws.Lambdas import Lambdas


class test_Update_Lambda_Functions(TestCase):

    def test_update_lambda_functions(self):
        code_path = Files.path_combine('.','..')

        targets = [
                    'gsbot_gsuite.lambdas.gdocs'    ,   #   gdocs.py    Lambda_GDocs    GDocs_Commands
                    'gsbot_gsuite.lambdas.slides'   ,   #   slides.py   Lambda_Slides   Slides_Commands

                   ]
        result = ""
        for target in targets:
            Lambdas(target).update_with_src(code_path)
            result += " • {0}\n".format(target)

        text        = ":hotsprings: [gsbot-gsuite] updated lambda functions"
        attachments = [{'text': result, 'color': 'good'}]
        slack_message(text, attachments)  # gs-bot-tests
        Dev.pprint(text, attachments)


if __name__ == '__main__':
    unittest.main()
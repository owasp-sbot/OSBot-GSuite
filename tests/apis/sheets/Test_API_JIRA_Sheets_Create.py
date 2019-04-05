from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from gsbot_gsuite.apis.sheets.API_Jira_Sheets_Create import API_Jira_Sheets_Create


class Test_API_JIRA_Sheets_Create(TestCase):
    def setUp(self):
        self.file_id = '1AOeZ0VN_iLnVDjpZE_CfOh5Mm0WV-17EGt8HPbw7d18'
        self.sheets_create = API_Jira_Sheets_Create(self.file_id)

    def test__init__(self):
        null_values = ['_gsheets', '_jira', '_jira_rest', '_elastic', '_sheet_name', '_sheet_name_backup', '_sheet_id', '_sheet_id_backup', 'slack_team_id', 'slack_channel']
        for item in null_values:
            assert self.sheets_create.get(item) is None



    # def test_get_sheet_contents(self):
    #     sheet_name = self.sheets_create.sheet_name()
    #     Dev.pprint(self.sheets_create.get_sheet_data(sheet_name))
    #     Dev.pprint(self.sheets_create.headers)

    def test_create_create_jira_tickets_object(self):
        sheet_data   = self.sheets_create.sheet_data()
        jira_actions = self.sheets_create.calculate_jira_actions(sheet_data)
        Dev.pprint(jira_actions)


    def test_update_sheet_with_status(self):
        sheet_data   = self.sheets_create.sheet_data()
        jira_actions = self.sheets_create.calculate_jira_actions(sheet_data)
        self.sheets_create.update_sheet_with_status(jira_actions)

    def test_execute_jira_actions(self):
        sheet_data = self.sheets_create.sheet_data()
        jira_actions = self.sheets_create.calculate_jira_actions(sheet_data)
        self.sheets_create.execute_jira_actions(jira_actions)
        self.sheets_create.update_sheet_with_status(jira_actions)

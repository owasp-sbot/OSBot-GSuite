from unittest import TestCase

from osbot_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Assert import Assert
from pbx_gs_python_utils.utils.Misc import Misc


class Method_Hooks:
    def __init__(self):
        import osbot_aws.helpers.Lambda_Helpers
        osbot_aws.helpers.Lambda_Helpers.slack_message = lambda text, attachments, channel: Method_Hooks.on_slack_message(text)

    @staticmethod
    def on_slack_message(text):
        Dev.pprint('.....')
        Dev.pprint(text)

Method_Hooks()

from osbot_gsuite.apis.sheets.API_Jira_Sheets_Sync import API_Jira_Sheets_Sync


class Test_API_Jira_Sheets_Sync(TestCase):

    def setUp(self):
        #self.file_id  = '1yDxu5YxL9FxY5wQ1EEQlAYGt3flIsm2VTyWwPny5RLA'
        #self.file_id ='1gc3jQelTJ8250kCZqOhqBOOZUywGOy3AiNC6cghgHak'
        self.file_id  = '1_Bwz6z34wALFGb1ILUXG8CtF1-Km6F9_sGXnAu4gewY'
        #self.file_id = '1eQbkiTexDq_LKGqYRdzs1i4sfYq_2lef8SbtKvFqbtQ' # check for data to update
        self.api_sync = API_Jira_Sheets_Sync(self.file_id)
        self.api_sync.set_slack_support('T7F3AUXGV', 'DDKUZTK6X')

    def test__init__(self):
        null_values = ['_gsheets', '_jira', '_jira_rest', '_sheet_name', '_sheet_name_backup',
                       '_sheet_id', '_sheet_id_backup']
        for item in null_values:
            assert getattr(self.api_sync,item) is None , "for {0}".format(item)
        assert self.api_sync.sheet_title        == 'Jira Data'
        assert self.api_sync.backup_sheet_title == 'original_jira_data'
        assert self.api_sync.headers            == []
        assert self.api_sync.gsuite_secret_id   == 'gsuite_gsbot_user'
        assert self.api_sync.elastic_secret_id  == 'elastic-jira-dev-2'
        assert self.api_sync.gsuite_secret_id   == 'gsuite_gsbot_user'

    #def test_elastic(self):
    #    assert self.api_sync.elastic().elastic.index == 'jira,it_assets,sec_project'

    def test_jira__gsheets(self):
        assert self.api_sync.jira().secrets_id == 'GS_BOT_GS_JIRA'
        assert type(self.api_sync.gsheets().gdrive.gsuite).__name__ == 'Resource'

    def test_message(self):
        Method_Hooks.on_slack_message = lambda text: Assert(text).is_equal(message)     # hook on_slack_message so that we can check it

        message = Misc.random_string_and_numbers(prefix='an message to test_')          # random message to send
        self.api_sync.log_message(message)                                              # call method that we will intercept the slack_message method

    def test_error(self):
        Method_Hooks.on_slack_message = lambda text: Assert(text).is_equal(':red_circle: test error from unit test')
        self.api_sync.log_error("test error from unit test")

    def test_sheet_name_backup(self):
        Dev.pprint(self.api_sync.sheet_name_backup())


    def test_convert_sheet_data_to_raw_data(self):
        sheet_data = self.api_sync.get_sheet_data(self.api_sync.sheet_name())
        raw_data = self.api_sync.convert_sheet_data_to_raw_data(sheet_data)
        Dev.pprint(raw_data)

    def test_color_code_cells_based_on_diff_status(self):
        sheet_data  = self.api_sync.get_sheet_data(self.api_sync.sheet_name())
        backup_data = self.api_sync.get_sheet_data(self.api_sync.sheet_name_backup())
        issues      = self.api_sync.get_jira_issues_in_sheet_data(sheet_data)
        diff_cells  = self.api_sync.diff_sheet_data_with_jira_data(sheet_data, backup_data, issues)
        result      = self.api_sync.color_code_cells_based_on_diff_status(diff_cells)
        #Dev.pprint(result)
        #Dev.pprint(diff_cells)


    def test_diff_sheet_data_with_jira_data(self):
        sheet_data  = self.api_sync.get_sheet_data(self.api_sync.sheet_name())
        backup_data = self.api_sync.get_sheet_data(self.api_sync.sheet_name_backup())
        issues     = self.api_sync.get_jira_issues_in_sheet_data(sheet_data)
        result     = self.api_sync.diff_sheet_data_with_jira_data(sheet_data, backup_data, issues)
        #Json.save_json('/tmp/tmp_diff_data.json', result)
        Dev.pprint(result)

    def test_get_issue_data(self):
        Dev.pprint(self.api_sync.get_issue_data('RISK-1573'))
        Dev.pprint(self.api_sync.get_issue_data('SL-118'))


    def test_get_jira_issues_in_sheet_data(self):
        sheet_data = self.api_sync.get_sheet_data(self.api_sync.sheet_name())
        issues = self.api_sync.get_jira_issues_in_sheet_data(sheet_data)
        Dev.pprint(len(issues))

    def test_get_sheet_data(self):
        result = self.api_sync.get_sheet_data(self.api_sync.sheet_name())
        Dev.pprint(result)

    def test_get_sheet_raw_data(self):
        result = self.api_sync.get_sheet_raw_data(self.api_sync.sheet_name())
        Dev.pprint(result)

    def test_update_sheet_data_with_jira_data(self):
        sheet_data = self.api_sync.get_sheet_data(self.api_sync.sheet_name())
        self.api_sync.update_sheet_data_with_jira_data(sheet_data)
        Dev.pprint(sheet_data)

    def test_update_file_with_raw_data(self):
        sheet_data = self.api_sync.get_sheet_data(self.api_sync.sheet_name())
        self.api_sync.update_sheet_data_with_jira_data(sheet_data)
        raw_data   = self.api_sync.convert_sheet_data_to_raw_data(sheet_data)
        self.api_sync.update_file_with_raw_data(raw_data)

    def test_sync_data_between_jira_and_sheet(self):
        diff_cells = self.api_sync.diff_cells()
        #Json.save_json('/tmp/tmp_diff_cells.json',diff_cells)
        #diff_cells = Json.load_json('/tmp/tmp_diff_cells.json')
        self.api_sync.sync_data_between_jira_and_sheet(diff_cells)

    def test_sync_sheet_with_jira__bad_file_id(self):
        self.api_sync.file_id = 'aaaa'
        Dev.pprint(self.api_sync.load_data_from_jira())

    def test_update_backup_data_with_new_jira_value(self):
        item = { 'backup_value': 'Test updated....xyz . DEMO TO GS',
                  'col_index': 1,
                  'field': 'Summary',
                  'jira_value': 'Test updated....xyz . DEMO TO GS',
                  'key': 'RISK-12',
                  'row_index': 1,
                  'sheet_value': 'Test updated....CHANGED',
                  'status': 'sheet_change'}
        result = self.api_sync.update_backup_data_with_new_jira_value(item)
        Dev.pprint(result)

    def test_get_graph_nodes(self):
        graph_name = 'graph_Y3Y'
        issues_ids = self.api_sync.get_graph_nodes(graph_name)
        issues = self.api_sync.get_issues_data(issues_ids)
        Dev.pprint(issues)

    def test_create_sheet_from_graph(self):
        graph_name = 'graph_Y3Y'
        folder = '1o-kpQ9sLzo0_wE13XcmnUuH7GNsHpdbp'
        domain = 'photobox.com'
        result = self.api_sync.create_sheet_from_graph(graph_name, domain, folder)
        Dev.pprint(result)



    def test_load_data_from_jira(self): Dev.pprint(self.api_sync.load_data_from_jira())
    def test_diff_sheet         (self): Dev.pprint(self.api_sync.diff_sheet         ())
    def test_sync_sheet         (self): Dev.pprint(self.api_sync.sync_sheet         ())

    # def test__lambda_update(self):
    #     Lambda('pbx_gs_python_utils.lambdas.gs.elastic_jira').update_with_src()



    def test_bug_sheet_not_created_from_graph(self):
        graph_name = 'graph_1BS'
        folder_to_save = '1o-kpQ9sLzo0_wE13XcmnUuH7GNsHpdbp'
        domain_to_share = 'photobox.com'
        #result = self.api_sync.gsheets().all_spreadsheets()
        result = self.api_sync.create_sheet_from_graph(graph_name, domain_to_share,folder_to_save)
        Dev.pprint(result)

    def test_bug__error_loading_sheet(self):
        #self.file_id = '1eQbkiTexDq_LKGqYRdzs1i4sfYq_2lef8SbtKvFqbtQ'

        self.api_sync.file_id = '1xIeV2eQb59EsiJoOUB1yOK3FY2LCvzMmTgvhAVXlEEI' # 'NoneType' object is not iterable

        Dev.pprint(self.api_sync.load_data_from_jira())



    def test_bug__error__sync_sheet(self):
        self.api_sync.file_id = '1MHU2Av4tI0FaktjWjbIpFH_zwb-804CAn-MQLuqaq1A'  # Error processing command `sync_sheet`: _JSONDecodeError('Expecting value: line 1 column 1 (char 0)',)_
        Dev.pprint(self.api_sync.sync_sheet())
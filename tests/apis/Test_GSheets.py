from unittest         import TestCase

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Misc import Misc

from osbot_gsuite.apis.GSheets import GSheets


class Test_GDrive(TestCase):
    def setUp(self):
        self.gsheets = GSheets()

    def test_ctor(self):
        spreadsheets = self.gsheets.spreadsheets
        Dev.pprint(spreadsheets)
        #assert spreadsheets._baseUrl == 'https://sheets.googleapis.com/'

    # Helper Methods

    def get_target_file_id(self):
        file_id  = self.gsheets.gdrive.find_by_name('Test sheet').get('id')
        return file_id

    # GSheets methods

    def test_all_spreadsheets(self):
        spreadsheets = self.gsheets.all_spreadsheets()
        Dev.pprint(spreadsheets)
        #assert len(spreadsheets) > 0

    def test_execute_requests(self):
        sheet_id = self.get_target_file_id()
        # this is one wat to add values via the execute requests workflow
        requests = [{   'updateCells': {
                                        'start': {'sheetId': 0, 'rowIndex': 11, 'columnIndex': 0},
                                        'rows': [
                                            {
                                                'values': [
                                                    {
                                                        'userEnteredValue': {'numberValue': 1},
                                                        'userEnteredFormat': {'backgroundColor': {'red': 1}}
                                                    }, {
                                                        'userEnteredValue': {'numberValue': 2},
                                                        'userEnteredFormat': {'backgroundColor': {'blue': 1}}
                                                    }, {
                                                        'userEnteredValue': {'numberValue': 3},
                                                        'userEnteredFormat': {'backgroundColor': {'green': 1}}
                                                    }
                                                ]
                                            }
                                        ],
                                        'fields': 'userEnteredValue,userEnteredFormat.backgroundColor'
                                    }
                                }]
        result = self.gsheets.execute_requests(sheet_id,requests)
        Dev.pprint(result)

    def test_create(self):
        name   = 'test spreadsheet creation 2'
        folder = '1o-kpQ9sLzo0_wE13XcmnUuH7GNsHpdbp'
        result = self.gsheets.create(name, folder)
        Dev.pprint(result)

    def test_create_and_share_with_domain(self):
        name    = 'test spreadsheet creation 3'
        folder  = '1o-kpQ9sLzo0_wE13XcmnUuH7GNsHpdbp'
        domain  = 'photobox.com'
        file_id = self.gsheets.create_and_share_with_domain(name, domain, folder)
        web_link = self.gsheets.gdrive.file_weblink(file_id)
        Dev.pprint(web_link)


    def test_sheet_create(self):
        file_id = self.get_target_file_id()
        title    = Misc.random_string_and_numbers(2,'from tests_')
        sheet_id = self.gsheets.sheets_add_sheet(file_id, title)
        assert len(set(self.gsheets.sheets_properties_by_title(file_id))) == 2
        self.gsheets.sheets_rename_sheet(file_id, sheet_id, 'temp title')
        self.gsheets.sheets_delete_sheet(file_id, sheet_id)
        assert len(set(self.gsheets.sheets_properties_by_title(file_id))) == 1







    def test_sheets_metadata(self):
        sheet_id = self.get_target_file_id()
        metadata = self.gsheets.sheets_metadata(sheet_id)
        sheets = metadata.get('sheets')

        assert sheets[0].get('properties').get('title') == 'Sheet1'

    def test_values(self):
        sheet_id = self.get_target_file_id()
        range    = "Sheet1!A2:D4"
        values = self.gsheets.get_values(sheet_id, range)
        assert values[0] == ['1 1', '1 2', '1 3']

    def test_set_values(self):
        sheet_id = self.get_target_file_id()
        range    = "Sheet1!B17:D18"
        values   = [ ["a","b","c"],[1,2,3]]
        result   = self.gsheets.set_values(sheet_id,range,values)
        assert result == {  'spreadsheetId' : '158e_ijqFk8vka1dLQ9WLlinrFr4Rb4yXbIMdAM0C87g',
                            'updatedCells'  : 6,
                            'updatedColumns': 3,
                            'updatedRange'  : 'Sheet1!B17:D18',
                            'updatedRows'   : 2 }
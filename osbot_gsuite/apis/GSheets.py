
from osbot_gsuite.apis.GDrive import GDrive
from osbot_gsuite.apis.GSheet import GSheet
from osbot_gsuite.apis.GSuite import GSuite
from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.decorators.methods.cache_on_self import cache_on_self


class GSheets:

    def __init__(self, gsuite_secret_id=None):
        self.gdrive           = GDrive(gsuite_secret_id)
        self.gsuite_secret_id = gsuite_secret_id

    @cache_on_self
    def spreadsheets(self):
        return GSuite(self.gsuite_secret_id).sheets_v4().spreadsheets()

    def batch_update(self, file_id, requests):
        body = {'requests': requests}
        return self.execute(self.spreadsheets().batchUpdate(spreadsheetId=file_id, body=body))

    def create(self, title, folder=None):
        return self.gdrive.file_create("application/vnd.google-apps.spreadsheet", title, folder)

    def create_and_share_with_domain(self, title, domain, folder=None):
        file_id = self.gdrive.file_create("application/vnd.google-apps.spreadsheet", title, folder)
        self.gdrive.file_share_with_domain(file_id, domain)
        return file_id


        #return self.execute(self.spreadsheets().create( body=body))


    def execute(self,command):
        return self.gdrive.execute(command)

    def execute_request(self, file_id, request):
        return self.batch_update(file_id, [request])

    def execute_requests(self, file_id, requests):
        return self.batch_update(file_id, requests)


    # def all_spreadsheets(self):
    #    mime_type_presentations = 'application/vnd.google-apps.spreadsheet'
    #    return self.gdrive.find_by_mime_type(mime_type_presentations)

    def sheets_metadata(self, file_id):
        return self.execute(self.spreadsheets().get(spreadsheetId=file_id))

    @index_by
    def sheets(self, file_id):
        sheets = {}
        for sheet in self.sheets_metadata(file_id=file_id).get('sheets'):
            properties         = sheet.get('properties')
            sheet_id           = properties.get('sheetId')
            sheet_name         = properties.get('title'  )
            sheets[sheet_name] = self.sheet(file_id=file_id, sheet_id=sheet_id, sheet_name=sheet_name)
            #print(sheet)
        return sheets

    def sheet(self, file_id, sheet_id, sheet_name):
        if file_id is not None and sheet_id is not None and sheet_name is not None:
            return GSheet(gsheets=self, file_id=file_id, sheet_id=sheet_id, sheet_name=sheet_name)

    def sheets_add_sheet(self, file_id, title):
        request = { "addSheet": { "properties": { "title": title } } }

        result  =  self.execute_request(file_id, [request])
        return result.get('replies')[0].get('addSheet').get('properties').get('sheetId')


    def sheets_delete_sheet(self, file_id, sheet_id):
        request = { "deleteSheet": { "sheetId": sheet_id } }

        return self.execute_request(file_id, [request])

    def sheets_rename_sheet(self, file_id, sheet_id, new_name):
        request = {"updateSheetProperties": { "properties": { "sheetId": sheet_id    ,
                                                              "title"  : new_name   },
                                              "fields"    :   "title"               }}
        return self.execute_request(file_id, [request])

    def sheets_properties_by_id(self, file_id):
        values = {}
        metadata = self.sheets_metadata(file_id)
        for sheet in metadata.get('sheets'):
           properties = sheet.get('properties')
           sheet_id   = properties.get('sheetId')
           values[sheet_id] = properties
        return values

    def sheets_properties_by_title(self, file_id):
        values = {}
        metadata = self.sheets_metadata(file_id)
        if metadata:
            for sheet in metadata.get('sheets'):
               properties = sheet.get('properties')
               sheet_id   = properties.get('title')
               values[sheet_id] = properties
            return values

    def request_cell_set_background_color(self, sheet_id, col, row, red, green, blue):
        return {'updateCells': { 'start': {'sheetId': sheet_id, 'rowIndex': row, 'columnIndex': col },
                                 'rows': [{'values': [ {'userEnteredFormat' : {'backgroundColor': {'red': red, 'blue': blue, 'green': green}}}] } ],
                                 'fields': 'userEnteredFormat.backgroundColor'}}

    def request_cell_set_value(self, sheet_id, col, row, value):
        return {'updateCells': { 'start': {'sheetId': sheet_id, 'rowIndex': row, 'columnIndex': col },
                                 'rows': [{'values': [ {'userEnteredValue': {'stringValue': value}}] } ],
                                 'fields': 'userEnteredValue'}}

    def request_clear_formatting(self, sheet_id):
        return { "updateCells": { "range" : {"sheetId": sheet_id },
                                  "fields": "userEnteredFormat"  }}

    def clear_values(self, file_id, sheet_name):
        sheet_range = "{0}!A1:Z".format(sheet_name)
        return self.execute(self.spreadsheets().values().clear(spreadsheetId=file_id, range=sheet_range))

    def get_values(self, file_id, range):
        if file_id and range:
            values = self.spreadsheets().values()
            result = self.execute(values.get(spreadsheetId = file_id , range = range    ))
            return result.get('values', [])
        return []

    def set_sheet_data(self, file_id, sheet_name, data):
        sheet_data = self.covert_raw_data_to_flat_objects(data)
        self.clear_values(file_id, sheet_name)
        return self.set_values(file_id, sheet_name, sheet_data)

    def set_values(self, file_id, sheet_range, values):
        value_input_option = 'USER_ENTERED' # vs 'RAW'
        body               = { 'values' : values }
        result = self.execute(self.spreadsheets().values().update( spreadsheetId    = file_id,
                                                                 range            = sheet_range,
                                                                 valueInputOption = value_input_option,
                                                                 body             = body))
        return result

    # this assumes that the first row contains the fields and the rest is the data items
    def get_values_as_objects(self, file_id, range_selector):
        raw_data = self.get_values(file_id, range_selector)
        return self.convert_raw_data_to_objects(raw_data)

    def convert_raw_data_to_objects(self, raw_data):
        values = []
        if raw_data:
            fields = raw_data.pop(0)
            if not fields:                    # if the first row is empty, then use the second row as the fields
                fields = raw_data.pop(0)

            for column in raw_data:
                item = {}
                for index, cell in enumerate(column):
                    item[fields[index]] = cell
                values.append(item)
        return values


    # helper methods
    def covert_raw_data_to_flat_objects(self, raw_data):
        sheet_data = []
        headers = list(raw_data[0].keys())

        sheet_data.append(headers)

        for item in raw_data:
            sheet_data.append(list(item.values()))

        # make sure every cell is a string
        for i, row in enumerate(sheet_data):
            for j, cell in enumerate(row):
                if cell is None:
                    sheet_data[i][j] = ''
                else:
                    sheet_data[i][j] = str(sheet_data[i][j])
        return sheet_data

    def format_headers(self, file_id, sheet_id, end_column):
        requests =  [   { "repeatCell": { "range": {  "sheetId": sheet_id,
                                                      "startRowIndex"  : 0,
                                                      "endRowIndex"    : 1,
                                                      "endColumnIndex" : end_column},
                                          "cell" : {  "userEnteredFormat": { "backgroundColor": { "red": 0.8, "green": 0.8, "blue": 0.8 },
                                                                             "horizontalAlignment" : "CENTER",
                                                                             "textFormat"  : { "foregroundColor": { "red": 0.0, "green": 0.0, "blue": 0.0 },
                                                                                               "fontSize": 12,
                                                                                               "bold": True } }},
                                          "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)" } },
                        { "updateSheetProperties": { "properties": { "sheetId": sheet_id,
                                                                     "gridProperties": { "frozenRowCount": 1 }},
                                                     "fields": "gridProperties.frozenRowCount"}} ]
        self.execute_requests(file_id,requests)
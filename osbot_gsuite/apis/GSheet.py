from osbot_gsuite.apis.GTypes import Merge_Type, Wrap_Strategy, RGB, Border_Style
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Str import str_join


class GSheet:

    def __init__(self, gsheets, file_id, sheet_id, sheet_name):
        self.gsheets            = gsheets
        self.file_id            = file_id
        self.sheet_id           = sheet_id
        self.sheet_name         = sheet_name
        self.requests           = []
        self.requests_committed = []
        self.requests_results   = []

    def __repr__(self):
        return f"[GSheet] {self.sheet_name} (id: {self.sheet_id})"

    def add_request(self, request):
        self.requests.append(request)
        return self

    def add_request_borders(self, col_start, row_start, col_end=None, row_end=None, color=None, style=Border_Style.SOLID_MEDIUM):    # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/request#UpdateBordersRequest
        color = color or RGB.BLACK                      # do this here to avoid the mutable warning when in ctor
        kwargs_range = {"col_start": col_start ,
                        "row_start": row_start ,
                        "col_end"  : col_end   ,
                        "row_end"  : row_end   }
        request = { "updateBorders": {"range" : self.format_range(**kwargs_range) ,
                                      "top"   : { "style": style  ,"color": color},
                                      "bottom": { "style": style  ,"color": color},
                                      "left"  : { "style": style  ,"color": color},
                                      "right" : { "style": style  ,"color": color}}}
                                      # innerHorizontal
                                      # innerVertical
        return self.add_request(request)

    def add_request_column_size(self, start_col, end_col, size):
        request = { "updateDimensionProperties": { "range"      : { "sheetId": self.sheet_id,"dimension": "COLUMNS",
                                                                  "startIndex": start_col,"endIndex": end_col },
                                                   "properties" : { "pixelSize": size},
                                                   "fields"     : "pixelSize" }}
        return self.add_request(request)

    def add_request_row_size(self, start_row, end_row, size):
        request = { "updateDimensionProperties": { "range"      : { "sheetId": self.sheet_id,"dimension": "ROWS",
                                                                  "startIndex": start_row,"endIndex": end_row },
                                                   "properties" : { "pixelSize": size},
                                                   "fields"     : "pixelSize" }}
        return self.add_request(request)

    def add_request_insert_column(self, start_col, end_col=None):
        start_index = start_col
        end_index   = end_col or start_col + 1
        request = { "insertDimension": { "range"      : { "sheetId": self.sheet_id,"dimension": "COLUMNS",
                                                          "startIndex": start_index,"endIndex": end_index },
                                        "inheritFromBefore": False }}
        return self.add_request(request)

    def add_request_insert_row(self, start_row, end_row=None):
        start_index = start_row
        end_index   = end_row or start_row + 1
        request = { "insertDimension": { "range"      : { "sheetId": self.sheet_id,"dimension": "ROWS",
                                                          "startIndex": start_index,"endIndex": end_index },
                                        "inheritFromBefore": False }}
        return self.add_request(request)

    def add_request_merge_cells(self, col_start, row_start, col_end=None, row_end=None, merge_type=Merge_Type.MERGE_ALL):
        kwargs_range = {"col_start": col_start ,
                        "row_start": row_start ,
                        "col_end"  : col_end   ,
                        "row_end"  : row_end   }
        request = { "mergeCells": {"range" : self.format_range(**kwargs_range) ,
                                      "mergeType"   : merge_type}}
        return self.add_request(request)

    def add_request_wrap_stategy(self,col_start, row_start, col_end=None, row_end=None, wrap_stategy=Wrap_Strategy.WRAP):
        kwargs_range = {"col_start": col_start ,
                        "row_start": row_start ,
                        "col_end"  : col_end   ,
                        "row_end"  : row_end   }
        request = { "updateCells"  : { "range": self.format_range(**kwargs_range) ,
                                       "rows": [{ "values": [ { "userEnteredFormat": { "wrapStrategy": wrap_stategy}}]}],
                    "fields"       :   "userEnteredFormat.wrapStrategy" }}
        request = {
			  "updateCells": {
				"range": {
				  "sheetId": self.sheet_id,
				  "startRowIndex": 0,
				  "startColumnIndex": 0,
                  "endRowIndex": 1,
                    "endColumnIndex": 1,
				},
				"rows": [
				  {
					"values": [
					  {
                          'userEnteredValue': {'stringValue': "value"},
						"userEnteredFormat": {
						  "wrapStrategy": wrap_stategy
						}
					  }
					]
				  }
				],
				"fields": "userEnteredValue.stringValue, userEnteredFormat.wrapStrategy"
			  }
			}


        pprint(request)
        self.add_request(request)
        return self
    def format_range(self, col_start, row_start, col_end=None, row_end=None):
        return { "sheetId"         : self.sheet_id              ,
                 "startRowIndex"   : row_start                  ,
                 "endRowIndex"     : row_end  or row_start + 1  ,  # default to only impacting the start_row_index
                 "startColumnIndex": col_start                  ,
                 "endColumnIndex"  : col_end  or col_start + 1  }  # default to only impacting the start_column_index

    def format_cell(self, background_color_rgb=None, foreground_color_rgb=None, text_align_horizontal=None, bold=False, font_size=None,wrap_strategy=None):
        textFormat      = {}
        cell            = {"textFormat": textFormat }
        fields        = []

        if background_color_rgb:
            cell['backgroundColor'] = background_color_rgb
            fields.append("backgroundColor")

        if bold is not None:
            textFormat['bold'] = bold
            fields.append("textFormat.bold")

        if text_align_horizontal:
            cell['horizontalAlignment'] = text_align_horizontal
            fields.append("horizontalAlignment")

        if font_size:
            textFormat['fontSize'] = font_size
            fields.append("textFormat.fontSize")

        if foreground_color_rgb:
            textFormat['foregroundColor'] = foreground_color_rgb
            fields.append("textFormat.foregroundColor")

        if wrap_strategy:
            cell['wrapStrategy'] = wrap_strategy
            fields.append("wrapStrategy")

        fields_format = f"userEnteredFormat({str_join(',',fields)})"
        cells_format  = {  "userEnteredFormat": cell }

        return cells_format, fields_format


    def request_format_cell(self, col_start, row_start, col_end=None, row_end=None, cell_color=None, text_color=None, text_align=None, bold=None, font_size=None, wrap_strategy=None):
        kwargs_range = {"col_start": col_start ,
                        "row_start": row_start ,
                        "col_end"  : col_end   ,
                        "row_end"  : row_end   }
        kwargs_cell  = {"background_color_rgb" : cell_color            ,
                        "foreground_color_rgb" : text_color            ,
                        "text_align_horizontal": text_align            ,
                        "bold"                 : bold                  ,
                        "font_size"            : font_size             ,
                        "wrap_strategy"        : wrap_strategy         }
        range        = self.format_range(**kwargs_range)
        cell, fields = self.format_cell(**kwargs_cell)
        return { "repeatCell": { "range" : range   ,
                                 "cell"  : cell    ,
                                 "fields": fields}},

    def bold(self, col_start, row_start, col_end=None, row_end=None, bold=True):
        kwargs_range = {"col_start": col_start ,
                        "row_start": row_start ,
                        "col_end"  : col_end   ,
                        "row_end"  : row_end   ,
                        "bold"     : bold      }
        request = self.request_format_cell(**kwargs_range)
        self.requests.append(request)
        return self

    def font_size(self, col_start, row_start, col_end=None, row_end=None, font_size=None):
        kwargs_range = {"col_start" : col_start      ,
                        "row_start" : row_start      ,
                        "col_end"   : col_end        ,
                        "row_end"   : row_end        ,
                        "font_size" : font_size      }
        request = self.request_format_cell(**kwargs_range)
        self.requests.append(request)
        return self

    def cell_color(self, col_start, row_start, col_end=None, row_end=None, cell_color=None):
        kwargs_range = {"col_start" : col_start      ,
                        "row_start" : row_start      ,
                        "col_end"   : col_end        ,
                        "row_end"   : row_end        ,
                        "cell_color" : cell_color      }
        request = self.request_format_cell(**kwargs_range)
        self.requests.append(request)
        return self

    def wrap_cells(self, col_start, row_start, col_end=None, row_end=None, wrap_strategy=Wrap_Strategy.WRAP):
        kwargs_range = {"col_start"     : col_start      ,
                        "row_start"     : row_start      ,
                        "col_end"       : col_end        ,
                        "row_end"       : row_end        ,
                        "wrap_strategy" : wrap_strategy      }
        request = self.request_format_cell(**kwargs_range)
        self.requests.append(request)
        return self

    def hide_grid_lines(self, value=True):
        request = {"updateSheetProperties": {"properties": {"sheetId": self.sheet_id,
                                                            "gridProperties": {"hideGridlines":value}},
                                             "fields": "gridProperties.hideGridlines"}}
        self.requests.append(request)
        return self

    def text_align(self, col_start, row_start, col_end=None, row_end=None, text_align=None):
        kwargs_range = {"col_start"  : col_start      ,
                        "row_start"  : row_start      ,
                        "col_end"    : col_end        ,
                        "row_end"    : row_end        ,
                        "text_align" : text_align      }
        request = self.request_format_cell(**kwargs_range)
        self.requests.append(request)
        return self

    def text_color(self, col_start, row_start, col_end=None, row_end=None, text_color=None):
        kwargs_range = {"col_start"  : col_start      ,
                        "row_start"  : row_start      ,
                        "col_end"    : col_end        ,
                        "row_end"    : row_end        ,
                        "text_color" : text_color      }
        request = self.request_format_cell(**kwargs_range)
        self.requests.append(request)
        return self

    def clear_formatting(self):
        self.requests.append(self.gsheets.request_clear_formatting(sheet_id=self.sheet_id))
        return self

    def set_value(self, col, row, value):
        request = self.gsheets.request_cell_set_value(sheet_id=self.sheet_id, col=col,row=row,  value=value)
        self.requests.append(request)
        return self

    def set_values(self, cells):
        for cell in cells:
            (col, row, value) = cell
            print(cell)
            self.set_value(col, row, value)
        return self

    def info(self):
        return { "file_id"              : self.file_id                ,
                 "sheet_id"             : self.sheet_id               ,
                 "sheet_name"           : self.sheet_name             ,
                 "# requests queued"    : len(self.requests          ),
                 "# requests committed" : len(self.requests_committed),
                 }

    def commit(self):
        if self.requests:
            self.gsheets.execute_requests(file_id=self.file_id, requests=self.requests)
            self.requests_committed.extend(self.requests)
            self.requests = []
            return True
        return False
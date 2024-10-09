from osbot_utils.utils.Objects import dict_to_obj

from osbot_gsuite.gsuite.docs.GDocs             import GDocs
from osbot_gsuite.gsuite.drive.GDrive import GDrive
from osbot_utils.base_classes.Type_Safe         import Type_Safe

from osbot_gsuite.apis.GTypes                   import Named_Style, Dash_Style, RGB, Width_Type, Alignment
from osbot_gsuite.apis.utils.GDoc_Named_Range   import GDoc_Named_Range
from osbot_utils.utils.Dev                      import pprint
from osbot_utils.utils.Misc                     import list_set

# good docs references:
#  - document structure: https://developers.google.com/docs/api/concepts/structure
#  - request object: https://developers.google.com/docs/api/reference/rest/v1/documents/request

class GDoc(Type_Safe):
    gdrive             : GDrive
    gdocs              : GDocs
    file_id            : str
    requests           : list
    requests_committed : list

    def add_request_delete_named_range(self, name=None, named_range_id=None):
        if name:
            request = {"deleteNamedRange": {"name":name}}
            self.requests.append(request)
        if named_range_id:
            request = {"deleteNamedRange": {"namedRangeId": named_range_id}}
            self.requests.append(request)
        return self

    def add_request_delete_table(self, table_index):
        tables = self.tables()
        if len(tables) > table_index:
            table = tables[table_index]
            self.add_request_delete_range(table)
        return self

    def add_requests_delete_tables(self):
        tables = self.tables()
        while tables and len(tables) >0:                       # do the updates in reverse so that we don't have to deal with changed start and end indexes
            table = tables.pop()
            self.add_request_delete_range(table)
        return self

    def add_request_delete_range(self, range, start_delta=0 , end_delta=0):
        start_index = range.get('start_index') + start_delta
        end_index   = range.get('end_index'  ) + end_delta
        if start_index and end_index:
            if end_index > start_index:
                request = {"deleteContentRange": {"range": { "startIndex": start_index, "endIndex": end_index } } }
                self.requests.append(request)
        return end_index - start_index

    def add_request_delete_table_column(self, table, column_index=0):
        table_start_index = table.get('start_index')
        request = { 'deleteTableColumn': { 'tableCellLocation': { 'tableStartLocation': { 'index': table_start_index },
                                                                  'columnIndex'       : column_index }}}
        self.requests.append(request)
        return self

    def add_request_delete_table_row(self, table, row_index=0):
        table_start_index = table.get('start_index')
        request = { 'deleteTableRow': { 'tableCellLocation': { 'tableStartLocation': { 'index': table_start_index },
                                                                'rowIndex'         : row_index }}}
        self.requests.append(request)
        return self

    def add_request_insert_inline_image(self, image_id, location, width=None, height=None):
        image_url = f'https://lh3.google.com/u/1/d/{image_id}'
        return self.add_request_insert_inline_image_from_image_url(image_url=image_url, location=location, width=width, height=height)

    def add_request_insert_inline_image_from_image_url(self, image_url, location, width=None, height=None):
        if type(image_url) is str and location > 0:
            location = {'index': location}
            object_size = {}
            if width:
                object_size["width"] = { 'magnitude': width, 'unit': 'PT'}
            if  height:
                object_size["height"] = {'magnitude': height, 'unit': 'PT'}
            request  = {'insertInlineImage': { 'location'  : location    ,
                                               'uri'       : image_url   ,
                                               'objectSize': object_size} }
            self.requests.append(request)
        return self

    def add_request_insert_table(self, rows, columns, location):
        request = { 'insertTable': { 'rows'     : rows,
                                     'columns'  : columns,
                                     'location' : {"segmentId": None, 'index': location }}}
        self.requests.append(request)
        return self

    def add_request_insert_table_column(self, table, column_index=0, insert_below=False):
        table_start_index = table.get('start_index')
        request = { 'insertTableColumn': { 'tableCellLocation': { 'tableStartLocation': { 'index': table_start_index },
                                                                  'columnIndex'          : column_index } ,

                                        'insertRight': insert_below }}
        self.requests.append(request)
        return self

    def add_request_insert_table_row(self, table, row_index=0, insert_below=False):
        table_start_index = table.get('start_index')
        request = { 'insertTableRow': { 'tableCellLocation': { 'tableStartLocation': { 'index': table_start_index },
                                                                'rowIndex'         : row_index } ,

                                        'insertBelow': insert_below }}
        self.requests.append(request)
        return self

    def add_request_insert_text(self, text, location):
        request = { "insertText" : { "text"      : text,
                                     "location" : {"segmentId": None, 'index': location }}}
        self.requests.append(request)
        return self

    def add_request_named_range_create(self, name, start_index, end_index):
        request = { "createNamedRange": {"name" : name  ,
                                         "range": { "startIndex": start_index, "endIndex": end_index } }}
        self.requests.append(request)
        return self

    def add_request_named_range_reset(self, name, start_index, end_index):
        self.add_request_delete_named_range(name=name)
        self.add_request_named_range_create(name=name, start_index=start_index, end_index=end_index)
        return self

    def add_request_page_break(self, location):
        request = { "insertPageBreak" : { "location" : {"segmentId": None, 'index': location }}}
        self.requests.append(request)
        return self

    def add_request_replace_range_text(self, range, text):
        start_index = range.get('start_index')
        self.add_request_delete_range(range)
        self.add_request_insert_text(text=text, location=start_index)
        return self

    # todo: this is not working reliably for tables
    def add_request_replace_ranges_text(self, ranges, start_index, new_text):
        for range in ranges:
            self.add_request_delete_range(range)
        self.add_request_insert_text(text=new_text, location=start_index)
        return self

    def add_request_replace_text(self, text_to_find, text_to_replace, match_case=True):
        request = { "replaceAllText" : { "replaceText"  : text_to_replace,
                                         "containsText" : {"text": text_to_find, 'matchCase': match_case }}}
        self.requests.append(request)
        return self

    def add_request_text_style(self, start_index, end_index, bold=False, italic=False, underline=False, strikethrough=False, smallCaps=False, background_color=None, foreground_color=None, font_family=None, font_size=None, baseline_offset=None, link=None):
        text_style = {'bold'          : bold         ,
                      'italic'        : italic       ,
                      'underline'     : underline    ,
                      'strikethrough' : strikethrough,
                      'smallCaps'     : smallCaps    ,
                      }
        if background_color : text_style['backgroundColor'   ] = {'color': {'rgbColor': background_color}}
        if foreground_color : text_style['foregroundColor'   ] = {'color': {'rgbColor': foreground_color}}
        if font_size        : text_style['fontSize'          ] = { "magnitude": font_size, "unit": 'PT'}
        if font_family      : text_style['weightedFontFamily'] = {'fontFamily' :font_family }
        if baseline_offset  : text_style['baselineOffset'    ] = baseline_offset
        if link             : text_style['link'              ] = {'url': link }

        #fields     = "*"
        fields = ",".join(list_set(text_style))
        range      = { "segmentId"  : None, "startIndex" : start_index, "endIndex"   : end_index}
        request    = { "updateTextStyle" : { "textStyle": text_style,
                                             "fields"   : fields    ,
                                             "range"    : range     }}
        self.requests.append(request)
        return self

    def add_request_text_style_clear(self, start_index, end_index):                                 # bug: see why it doesn't work when document is empty
        range      = { "segmentId"  : None, "startIndex" : start_index, "endIndex"   : end_index}
        request    = { "updateTextStyle" : { "textStyle": {},
                                             "fields"   : '*'    ,
                                             "range"    : range     }}
        self.requests.append(request)
        return self

    def add_request_paragraph_style(self,start_index, end_index, alignment=None, named_style=None, line_spacing=None, direction=None,
                                    spacing_mode = None, space_above=None, space_below=None, border=None, indent_first_line=None,
                                    indent_start=None, indent_end=None, shading=None):
        paragraph_style = { "namedStyleType" : Named_Style.NORMAL_TEXT       # seems like this always need to be set or we get an error "Named style property is not inherited and cannot be cleared"
                          }
        if alignment    : paragraph_style['alignment'      ] = alignment
        if named_style  : paragraph_style['namedStyleType' ] = named_style or Named_Style.NORMAL_TEXT
        if line_spacing : paragraph_style['lineSpacing'    ] = line_spacing
        if direction    : paragraph_style['direction'      ] = direction
        if spacing_mode : paragraph_style['spacingMode'    ] =  spacing_mode
        if space_above  : paragraph_style['spaceAbove'     ] = { "magnitude": space_above, "unit": 'PT'}
        if space_below  : paragraph_style['spaceBelow'     ] = { "magnitude": space_below, "unit": 'PT'}

        self.format_border(paragraph_style, border)

        # if border       :
        #     border_size       = border.get('size'      , 1)
        #     border_padding    = border.get('padding'   , 1)
        #     border_dash_style = border.get('dash_style', Dash_Style.SOLID)
        #     border_color      = border.get('color'     , RGB.BLACK)
        #     border_style = { "color"     : {"color": {"rgbColor": border_color       }},
        #                      "width"     : {"magnitude": border_size   , "unit": 'PT'} ,
        #                      "padding"   : {"magnitude": border_padding, "unit": 'PT'} ,
        #                      "dashStyle" : border_dash_style}
        #     #paragraph_style['borderBetween'] = border_style            # this could have weird side effects
        #     paragraph_style['borderTop'   ] = border_style
        #     paragraph_style['borderLeft'  ] = border_style
        #     paragraph_style['borderRight' ] = border_style
        #     paragraph_style['borderBottom'] = border_style

        if indent_first_line: paragraph_style['indentFirstLine' ] = { "magnitude"     : indent_first_line, "unit": 'PT'}
        if indent_start     : paragraph_style['indentStart'     ] = {"magnitude"      : indent_start, "unit": 'PT'}
        if indent_end       : paragraph_style['indentEnd'       ] = {"magnitude"      : indent_end, "unit": 'PT'}
        if shading          : paragraph_style['shading'         ] = {"backgroundColor": {"color": {"rgbColor": shading }}}

        fields     = ",".join(list_set(paragraph_style)) # *  # using * was causing errors when updating paragraphs inside tables
        range      = { "segmentId": None, "startIndex": start_index, "endIndex": end_index}
        request    = { "updateParagraphStyle" : { "paragraphStyle": paragraph_style        ,
                                                  "fields"        : fields                 ,
                                                  "range"         : range                 }}
        self.requests.append(request)
        return self

    def add_request_merge_cells(self, table, column_index, row_index, column_span, row_span):
        table_start_index = table.get('start_index')
        request = { "mergeTableCells": { "tableRange": { "columnSpan": column_span,
                                                         "rowSpan"   : row_span   ,
                                                         "tableCellLocation": { "columnIndex"       : column_index,
                                                                                "rowIndex"          : row_index   ,
                                                                                "tableStartLocation": {'index': table_start_index}}}}}
        self.requests.append(request)
        return self

    def add_request_unmerge_cells(self, table, column_index, row_index, column_span, row_span):
        table_start_index = table.get('start_index')
        request = { "unmergeTableCells": { "tableRange": { "columnSpan": column_span,
                                                          "rowSpan"    : row_span   ,
                                                          "tableCellLocation": { "columnIndex"       : column_index,
                                                                                 "rowIndex"          : row_index   ,
                                                                                 "tableStartLocation": {'index': table_start_index}}}}}
        self.requests.append(request)
        return self

    def add_request_replace_named_range_content(self, text, name=None, named_range_id=None):
        if name:
            request = {"replaceNamedRangeContent": {"namedRangeName":name , "text": text}}
            self.requests.append(request)
        elif named_range_id:
            request = {"replaceNamedRangeContent": {"namedRangeName": named_range_id, "text": text}}
            self.requests.append(request)
        return self

    def add_request_text_style_to_range(self, range, kwargs_text_style=None):
        start_index = range.get('start_index') or range.get('startIndex')
        end_index   = range.get('end_index'  ) or range.get('endIndex')
        if kwargs_text_style is None:
            kwargs_text_style = {}              # which will remove all formatting
        if end_index and start_index and end_index > start_index:
            kwargs_text_style["start_index"] = start_index
            kwargs_text_style["end_index"  ] = end_index
            self.add_request_text_style(**kwargs_text_style)
        return self

    def add_request_paragraph_style_to_range(self, range, kwargs_paragraph_style=None):
        start_index = range.get('start_index') or range.get('startIndex')
        end_index   = range.get('end_index'  ) or range.get('endIndex')
        if kwargs_paragraph_style is None:
            kwargs_paragraph_style = {}              # which will remove all formatting
        if start_index and start_index:
            kwargs_paragraph_style["start_index"] = start_index
            kwargs_paragraph_style["end_index"  ] = end_index
            self.add_request_paragraph_style(**kwargs_paragraph_style)
        return self

    def add_requests_paragraph_style_to_ranges(self, ranges, kwargs_paragraph_style=None):
        for range in ranges:
            self.add_request_paragraph_style_to_range(range, kwargs_paragraph_style)
        return self

    def add_requests_text_style_to_ranges(self, ranges, kwargs_text_formatting):
        for range in ranges:
            self.add_request_text_style_to_range(range, kwargs_text_formatting)
        return self

    def add_request_update_table_cell_style(self, table, column_index, row_index, column_span=1, row_span=1,
                                                  background_color=None, padding=None, border=None, content_alignment=None):
        table_start_index = table.get('start_index')
        table_cell_style  = {}

        if background_color  : table_cell_style['backgroundColor'] = { "color": { "rgbColor": background_color}}
        if content_alignment : table_cell_style['contentAlignment'] = content_alignment
        if padding:
            table_cell_style['paddingTop'   ] = {'magnitude': padding, 'unit': 'PT'}   # for now use the same value for all sides
            table_cell_style['paddingLeft'  ] = {'magnitude': padding, 'unit': 'PT'}
            table_cell_style['paddingBottom'] = {'magnitude': padding, 'unit': 'PT'}
            table_cell_style['paddingRight' ] = {'magnitude': padding, 'unit': 'PT'}
        self.format_border(table_cell_style, border)

        fields = ",".join(list_set(table_cell_style))
        if fields:
            request = { "updateTableCellStyle": { "tableCellStyle": table_cell_style,
                                                  "fields"        : fields,
                                                  "tableRange"    : { "columnSpan": column_span,
                                                                      "rowSpan"   : row_span   ,
                                                                      "tableCellLocation": { "columnIndex"       : column_index,
                                                                                             "rowIndex"          : row_index   ,
                                                                                             'tableStartLocation': {'index': table_start_index}}}}}
            self.requests.append(request)
        return self

    def add_request_update_table_column_width(self, table, width, columns=None, width_type=None):
        table_start_index = table.get('start_index')
        request = { 'updateTableColumnProperties': { 'tableStartLocation'   : {'index': table_start_index},
                                                     'columnIndices'        : columns or []               ,
                                                     'tableColumnProperties': { 'widthType': width_type or Width_Type.FIXED_WIDTH,
                                                                                'width': { 'magnitude': width, 'unit': 'PT' }},
                                                     'fields': '*'}}
        self.requests.append(request)
        return self

    def add_request_update_table_row_height(self, table, height, rows=None):
        table_start_index = table.get('start_index')
        request = { 'updateTableRowStyle': { 'tableStartLocation': {'index': table_start_index},
                                             'rowIndices'        : rows or []                  ,
                                             'tableRowStyle'     : { 'minRowHeight': { 'magnitude': height, 'unit': 'PT' }},
                                             'fields'            : '*'}}
        self.requests.append(request)
        return self



    def format_border(self, target, border):
        if border:
            border_size       = border.get('size'      , 1)
            border_padding    = border.get('padding')
            border_dash_style = border.get('dash_style', Dash_Style.SOLID)
            border_color      = border.get('color'     , RGB.BLACK)
            border_style = { "color"     : {"color": {"rgbColor": border_color       }},
                             "width"     : {"magnitude": border_size   , "unit": 'PT'} ,
                             "dashStyle" : border_dash_style}
            if border_padding:
                border_style['padding'] = {"magnitude": border_padding, "unit": 'PT'}
            #target['borderBetween'] = border_style            # this could have weird side effects
            target['borderTop'   ] = border_style
            target['borderLeft'  ] = border_style
            target['borderRight' ] = border_style
            target['borderBottom'] = border_style
        return self

    def commit(self):
        if len(self.requests) > 0:
            #print(f'[commit] {len(self.requests)} requests')
            results = self.gdocs.execute_requests(file_id=self.file_id, requests=self.requests)
            self.requests_committed.extend(self.requests)
            self.requests = []
            return results.get('replies')
        return []

    def info(self):
        info =  self.gdrive.file_metadata(file_id=self.file_id)
        return { "file_id"              : self.file_id                 ,
                 "file_name"            : info.get('name')             ,
                 "# requests queued"    : len(self.requests           ),
                 "# requests committed" : len(self.requests_committed )}

    def info_all(self):
        return self.gdrive.file_metadata(file_id=self.file_id, fields='*')

    def insert_text(self, text, location):
        return self.add_request_insert_text(text=text, location=location)

    def file_name(self):
        return self.info().get('file_name')

    def file_name_update(self, new_name):
        body = {'name' : new_name}
        return self.gdrive.file_update(file_id=self.file_id, body=body)

    # def named_ranges(self, name):
    #     data =  self.named_ranges_info(name).get('namedRanges', [])
    #     ranges = []
    #     for item in data:
    #         for range in item.get('ranges'):
    #             ranges.append(range)
    #     return ranges

    # def named_ranges_info(self, name):
    #     return self.named_ranges_list().get(name,{})

    def named_range(self, named_range_name):
        return GDoc_Named_Range(gdoc=self, named_range_name=named_range_name)

    def named_range_paragraph_style(self, name, paragraph_style):
        for entry in self.named_ranges(name):
            for range in entry.get('ranges'):
                self.add_request_paragraph_style_to_range(range=range, kwargs_paragraph_style=paragraph_style)
        return self.commit()

    def named_range_clear_style(self, name):
        for entry in self.named_ranges(name):
            for range in entry.get('ranges'):
                self.add_request_paragraph_style_to_range(range=range, kwargs_paragraph_style={})
                self.add_request_text_style_to_range     (range=range, kwargs_text_style     ={})

        return self.commit()

    def named_range_text_style(self, name, text_style):
        named_range = self.named_ranges(name)
        for entry in named_range:
            for range in entry.get('ranges'):
                self.add_request_text_style_to_range(range=range, kwargs_text_style=text_style)
        return self.commit()

    def named_range_set_text(self, name, text, named_range_id=None):
        self.add_request_replace_named_range_content(text=text, name=name,named_range_id=named_range_id)
        return self.commit()

    def named_range_ranges(self, name):
        ranges = []
        for item in self.named_ranges(name):
            ranges.extend(item.get('ranges'))
        return ranges

    def named_ranges(self, name=None):
        doc          = self.document()
        named_ranges =  doc.get('namedRanges',{})
        mappings     = {}
        for named_range_name, entry in named_ranges.items():
            mappings[named_range_name] = entry.get('namedRanges')

        if name:
            return mappings.get(name, [])
        return mappings

    def named_ranges_info(self):
        mappings = {}
        for named_range_name, entries in self.named_ranges().items():
            all_ranges = []
            for entry in entries:
                all_ranges.extend(entry.get('ranges'))
            mappings[named_range_name] = { "range"      : self.ranges_start_and_end(all_ranges),
                                           "all_ranges" : all_ranges                           }
        return mappings

    def named_ranges_create(self, name, start_index, end_index):
        self.add_request_named_range_create(name=name, start_index=start_index, end_index=end_index)
        result = self.commit()
        if len(result) > 0:
            return result.pop().get('createNamedRange',{}).get('namedRangeId')

    def named_ranges_delete(self, name, named_range_id=None):
        self.add_request_delete_named_range(name=name,named_range_id=named_range_id)
        return self.commit()

    def named_ranges_delete_all(self):
        for named_range_name in list_set(self.named_ranges()):
            self.add_request_delete_named_range(name=named_range_name)
        return self.commit()

    # using document json data/contents

    def body(self):
        return self.document().body

    def content_group_by_entry_type(self, mappings, entry):
        start_index = entry.get('startIndex')
        end_index   = entry.get('endIndex')
        for key, value in entry.items():
            if key in ['startIndex', 'endIndex']:
                continue
            entry_type  = key
            value["start_index"] = start_index
            value["end_index"  ] = end_index
            if mappings.get(entry_type) is None:
                mappings[entry_type] = []
            mappings[entry_type].append(value)

    def body_contents(self):
        content = self.body().get('content', [])
        mappings = {}
        for entry in content:
            self.content_group_by_entry_type(mappings, entry)
        return mappings

    def document(self, fields=None):
        data = self.gdocs.documents().get(documentId=self.file_id, fields=fields).execute()
        return dict_to_obj(data)

    def document_end_index(self):
        return self.document_range().get('end_index')

    def document_range(self):
        fields = "body.content(start_index,end_index)"  # todo: see what is the performance improvement in doing this for large documents
        data   = self.document(fields=fields)           #       there should be one
        start_index = None
        end_index   = None
        for range in data.get('body').get('content'):   # todo: find a better way to do this
            if start_index is None:
                start_index = range.get('startIndex')
            end_index = range.get('endIndex')
        return {"start_index": start_index, "end_index": end_index - 1}

    def document_clear(self, delete_named_ranges=True):
        range = self.document_range()
        default_paragraph_style = {"named_style":Named_Style.NORMAL_TEXT,"alignment": Alignment.START}
        self.add_request_paragraph_style_to_range(range, default_paragraph_style)
        self.add_request_text_style_to_range(range, {})
        self.add_request_delete_range(range)
        if delete_named_ranges:
            return self.named_ranges_delete_all()           # this will trigger the commit
        else:
            return self.commit()

    # def document_clear_formating(self):
    #     #range = self.document_range()
    # #
    #     self.commit()

    def inline_objects(self):
        mappings = {}
        for key, inline_object in self.document().get('inlineObjects').items():
            properties = inline_object.get('inlineObjectProperties', {})            # remove redundant inlineObjectProperties node
            data       = properties.get('embeddedObject')                           # and embeddedObject
            mappings[key] = data
        return mappings

    def paragraphs(self):
        return self.body_contents().get('paragraph')

    def paragraphs_elements(self):
        paragraphs = self.paragraphs()
        mappings = {}
        for paragraph in paragraphs:
            for entry in paragraph.get('elements',[]):
                self.content_group_by_entry_type(mappings, entry)
        return mappings

    def pdf__file(self, file_path):
        return self.gdrive.file_export_as_pdf_to(self.file_id, file_path)

    def pdf__bytes(self):
        return self.gdrive.file_export(file_id=self.file_id)

    def table_cells(self, table):
        table_texts = self.table_paragraph_elements_text_runs_content(table)
        cells = []
        for row in table_texts:
            for cell in row:
                cells.append(cell)
        return cells

    def table_column(self, table, column_index):
        column_data = []
        table_texts = self.table_paragraph_elements_text_runs_content(table)
        for row in table_texts:
            if len(row) > column_index:
                cell = row[column_index]
                column_data.append(cell)
        return column_data

    def table_row(self, table, row_index):
        table_texts = self.table_paragraph_elements_text_runs_content(table)
        if len(table_texts) > row_index:
            return table_texts[row_index]

    def table_paragraph_elements_text_runs_content(self, table):
        rows = []
        if table:
            for table_rows in table.get('tableRows'):
                row = []
                for table_cell in table_rows.get('tableCells'):
                    content = table_cell.get('content')
                    text_runs = []
                    for item in content:
                        paragraph = item.get('paragraph')
                        for element in paragraph.get('elements'):
                            text_run = {"start_index": element.get('startIndex'),
                                        "end_index"  : element.get('endIndex'),
                                        "content"    : element.get('textRun').get('content')}
                            text_runs.append(text_run)
                    cell = { "start_index": table_cell.get('startIndex'),
                             "end_index"  : table_cell.get('endIndex'),
                             "text_runs"  : text_runs,
                             "range"      : self.ranges_start_and_end(text_runs)}
                    row.append(cell)
                rows.append(row)
        return rows

    def tables(self):
        return self.body_contents().get('table')

    def text_runs(self):
        return self.paragraphs_elements().get('textRun')

    def text_runs_find_text(self, text, exact_match=False):
        matches = []
        for text_run in self.text_runs():
            if text in text_run.get('content'):
                if exact_match:
                    if text != text_run.get('content'):
                        continue
                matches.append(text_run)
        return matches

    def ranges_start_and_end(self, ranges):
        start_index  = None
        end_index    = None
        content_size = 0
        for range in ranges:                            # todo: see if there a better way to do this (just read the first and last one)
            if start_index is None:
                start_index = range.get('start_index') or range.get('startIndex')
            end_index = range.get('endIndex') or range.get('end_index')
        content_size = end_index - start_index
        return {"start_index": start_index, "end_index": end_index , "content_size": content_size}
    # utils


from osbot_gsuite.apis.GDrive import GDrive

#docs for request https://developers.google.com/docs/api/reference/rest/v1/documents/request
from osbot_gsuite.apis.GTypes import Named_Style, Alignment, Dash_Style, RGB
from osbot_utils.utils.Dev import pprint


class GDoc:

    def __init__(self, gdocs, file_id):
        self.gdrive             = GDrive()
        self.gdocs              = gdocs
        self.file_id            = file_id
        self.requests           = []
        self.requests_committed = []

    def add_request_insert_inline_image(self, image_id):
        image_url = f'https://lh3.google.com/u/1/d/{image_id}'
        return self.add_request_insert_inline_image_from_file_id(image_url=image_url)

    def add_request_insert_inline_image_from_file_id(self, image_url):
        location = {'index': 1}
        height   = { 'magnitude': 250, 'unit': 'PT'}
        width    = { 'magnitude': 250,'unit': 'PT'}
        request  = {'insertInlineImage': { 'location'  : location    ,
                                           'uri'       : image_url   ,
                                           'objectSize': { 'height': height, 'width': width}} }

        self.requests.append(request)
        return self

    def add_request_insert_text(self, text, location):
        request = { "insertText" : { "text"      : text,
                                     "location" : {"segmentId": None, 'index': location }}}
        self.requests.append(request)
        return self

    def add_request_named_range_create(self, name, range):
        request ={"createNamedRange": {"name" : name  , "range": range }}
        self.requests.append(request)
        return self

    def add_request_page_break(self, location):
        request = { "insertPageBreak" : { "location" : {"segmentId": None, 'index': location }}}
        self.requests.append(request)
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

        fields     = "*"
        range      = { "segmentId"  : None, "startIndex" : start_index, "endIndex"   : end_index}
        request    = { "updateTextStyle" : { "textStyle": text_style,
                                             "fields"   : fields    ,
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
        if border       :
            border_size       = border.get('size'      , 1)
            border_padding    = border.get('padding'   , 1)
            border_dash_style = border.get('dash_style', Dash_Style.SOLID)
            border_color      = border.get('color'     , RGB.GREEN)
            border_style = { "color"     : {"color": {"rgbColor": border_color       }},
                             "width"     : {"magnitude": border_size   , "unit": 'PT'} ,
                             "padding"   : {"magnitude": border_padding, "unit": 'PT'} ,
                             "dashStyle" : border_dash_style}
            #paragraph_style['borderBetween'] = border_style            # this could have weird side effects
            paragraph_style['borderTop'  ] = border_style
            paragraph_style['borderLeft'] = border_style
            paragraph_style['borderRight'] = border_style
            paragraph_style['borderBottom'] = border_style

        if indent_first_line: paragraph_style['indentFirstLine' ] = { "magnitude"     : indent_first_line, "unit": 'PT'}
        if indent_start     : paragraph_style['indentStart'     ] = {"magnitude"      : indent_start, "unit": 'PT'}
        if indent_end       : paragraph_style['indentEnd'       ] = {"magnitude"      : indent_end, "unit": 'PT'}
        if shading          : paragraph_style['shading'         ] = {"backgroundColor": {"color": {"rgbColor": shading }}}

        fields     = "*"
        range      = { "segmentId": None, "startIndex": start_index, "endIndex": end_index}
        request    = { "updateParagraphStyle" : { "paragraphStyle": paragraph_style        ,
                                                  "fields"        : fields                 ,
                                                  "range"         : range                 }}
        self.requests.append(request)
        return self

    def commit(self):
        results = self.gdocs.execute_requests(file_id=self.file_id, requests=self.requests)
        #print(results)
        self.requests_committed.extend(self.requests)
        self.requests = []
        return results.get('replies')

    def document(self):
        return self.gdocs.docs.get(documentId=self.file_id).execute()

    def info(self):
        info =  self.gdrive.file_metadata(file_id=self.file_id)
        return { "file_id"              : self.file_id                 ,
                 "file_name"            : info.get('name')             ,
                 "# requests queued"    : len(self.requests           ),
                 "# requests committed" : len(self.requests_committed )}

    def info_all(self):
        return self.gdrive.file_metadata(file_id=self.file_id, fields='*')

    def file_name(self):
        return self.info().get('file_name')

    def file_name_update(self, new_name):
        body = {'name' : new_name}
        #    fileId: fileId,
            #resource: {name: "updated title"},
        return self.gdrive.file_update(file_id=self.file_id, body=body)

    def named_ranges(self, name):
        data =  self.named_ranges_info(name).get('namedRanges', [])
        ranges = []
        for item in data:
            for range in item.get('ranges'):
                ranges.append(range)
        return ranges

    def named_ranges_info(self, name):
        return self.named_ranges_list().get(name,{})

    def named_ranges_list(self):
        doc = self.document()
        return doc.get('namedRanges',{})

    def named_ranges_create(self, name, range):
        result = self.add_request_named_range_create(name=name, range=range).commit()
        if len(result) > 0:
            return result.pop().get('createNamedRange',{}).get('namedRangeId')
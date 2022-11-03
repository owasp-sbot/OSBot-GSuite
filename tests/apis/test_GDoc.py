from unittest import TestCase

from osbot_gsuite.apis.GDoc import GDoc
from osbot_gsuite.apis.GDocs import GDocs
from osbot_gsuite.apis.GTypes import RGB, Font_Family, Baseline_Offset, Alignment, Named_Style, Direction, Spacing_Mode, \
    Dash_Style
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Json import json_dump
from osbot_utils.utils.Lists import list_del
from osbot_utils.utils.Misc import list_set


class test_GDoc(TestCase):

    def setUp(self):
        self.file_id = '1dzCouTrwe5WgsAPXiF5JYmj1vsrmYqPgpjcycbLNY2s'
        self.gdocs   = GDocs()
        self.gdoc    = GDoc(gdocs=self.gdocs, file_id=self.file_id)

    def test_add_request_insert_table(self):
        result = self.gdoc.add_request_insert_table(3,5, 100).commit()
        pprint(result)

    def test_add_request_insert_text(self):
        result = self.gdoc.add_request_insert_text('----abc-----', 1).commit()
        pprint(result)


    def test_add_request_delete_range(self):
        result = self.gdoc.add_request_delete_range(1,4).commit()
        pprint(result)

    def test_add_request_page_break(self):
        result = self.gdoc.add_request_page_break(40).commit()
        pprint(result)

    def test_add_request_replace_text(self):
        kwargs = { "text_to_find"    : '{{here}}'                 ,
                   "text_to_replace" : 'replaced content {{here}}',
                    "match_case"     : True                       }
        result = self.gdoc.add_request_replace_text(**kwargs).commit()
        pprint(result)

    def test_add_request_text_style(self):
        kwargs = {"start_index"      : 1                       ,
                  "end_index"        : 20                      ,
                  "bold"             : True                    ,
                  "italic"           : True                    ,
                  "underline"        : True                    ,
                  "strikethrough"    : True                    ,
                  "smallCaps"        : True                    , # this doesn't seem to be working
                  "background_color" : RGB.DARK_BLUE_2         ,
                  "foreground_color" : RGB.WHITE               ,
                  "font_family"      : Font_Family.VERDANA     ,
                  "font_size"        : 20                      ,
                  "baseline_offset"  : Baseline_Offset.NONE    ,
                  "link"             : 'https://www.google.com'}
        result = self.gdoc.add_request_text_style(**kwargs).commit()
        pprint(result)

    def test_add_request_paragraph_style(self):
        kwargs = {"start_index"      : 20                              ,
                  "end_index"        : 30                              ,
                  "alignment"        : Alignment.JUSTIFIED                ,
                  "named_style"      : Named_Style.TITLE               ,
                  "line_spacing"     : 100                             ,
                  "direction"        : Direction.LEFT_TO_RIGHT         ,
                  "spacing_mode"     : Spacing_Mode.NEVER_COLLAPSE     ,
                  "space_above"      : 20                              ,
                  "space_below"      : 20                              ,
                  "border"           : { "color": RGB.RED             ,
                                         "size":2, "padding": 10      ,
                                         "dash_style": Dash_Style.DOT },
                  "indent_first_line": 20                             ,
                  "indent_start"     : 20                             ,
                  "indent_end"       : 20                             ,
                  "shading"          : RGB.GRAY                       ,
                  }
        result = self.gdoc.add_request_paragraph_style(**kwargs).commit()
        pprint(result)

    def test_info(self):
        result = self.gdoc.info()

        pprint(result)

    def test_info_all(self):
        result = self.gdoc.info_all()
        pprint(result)

    def test_file_name(self):
        result = self.gdoc.file_name()
        pprint(result)

    def test_file_name_update(self):
        new_name = 'New Name (ABC)'
        result = self.gdoc.file_name_update(new_name=new_name)
        pprint(result)

    def test_named_ranges(self):
        name = 'the name of the range'
        #name = 'another range v2'
        # range = { "segmentId"  : None,
        #           "startIndex" : 1,
        #           "endIndex"   : 10}
        # result = self.gdoc.named_ranges_create(name, range)
        result = self.gdoc.named_ranges(name)
        pprint(result)
        #'kix.ntntf5ko1m24'


    # using document json data/contents

    def test_document(self):
        result = self.gdoc.document()
        pprint(result)

    def test_body_contents(self):
        result = self.gdoc.body_contents()
        pprint(result)
        #pprint(list_set(result))

    def test_inline_objects(self):
        result= self.gdoc.inline_objects()
        pprint(result)
        "kix.se4xwuh4zgqc"

    def test_paragraphs(self):
        result = self.gdoc.paragraphs()
        pprint(result)

    def test_paragraphs_elements(self):
        result = self.gdoc.paragraphs_elements()
        pprint(result)

    def test_text_runs(self):
        result = self.gdoc.text_runs()
        pprint(result)

    def test_text_runs_find_text(self):
        text_to_find = 'to-find'
        matches = self.gdoc.text_runs_find_text(text_to_find, exact_match=False)
        pprint(matches)
        kwargs_formatting = {"bold": True , "foreground_color": RGB.RED}
        self.gdoc.add_requests_text_style_to_ranges(matches, kwargs_formatting).commit()

    def test_tables(self):
        result = self.gdoc.tables()
        table = result.pop(0)
        #kwargs_formatting = {"bold": True, "foreground_color": RGB.RED, 'font_size': 10}
        #self.gdoc.add_requests_text_style_to_range(table, kwargs_formatting).commit()
        pprint(table)




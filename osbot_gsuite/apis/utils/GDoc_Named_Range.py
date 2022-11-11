from googleapiclient.errors import HttpError

from osbot_utils.utils.Dev import pprint


class GDoc_Named_Range:

    def __init__(self, gdoc, named_range_name):
        self.gdoc             = gdoc
        self.named_range_name = named_range_name
        self.replies          = []
        self.start_index      = None
        self.end_index        = None

    def __enter__(self):
        self.set_range_indexes()
        self.gdoc.requests = []
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"[GDoc_Named_Range] executing {len(self.gdoc.requests)} requests")
        if exc_type:
            return False
        try:
            self.replies = self.gdoc.commit()
        except HttpError as error:
            print('\n[GDoc commit() Error]:', error.error_details)
            print(type(error))
            raise Exception(error)
        return True

    def add_text(self, text, location):
        if self.start_index < location < self.end_index:
            self.gdoc.insert_text(text=text, location=location)
        return self

    def append_image(self, image_url,width=None, height=None):
        if self.end_index:
            self.gdoc.add_request_insert_inline_image_from_image_url(image_url=image_url, location=self.end_index, width=width, height=height)
            self.end_index += 1
            self.reset_named_range()            # need to reset because the end index needs to be adjusted
        return self

    def append_table(self, rows, columns):
        if self.end_index:
            self.gdoc.add_request_insert_table(rows=rows, columns=columns, location=self.end_index)

    def append_text(self, text):
        if self.end_index and len(text) > 0:
            self.gdoc.insert_text(text=text, location=self.end_index)
            self.end_index += len(text)
            self.reset_named_range()            # need to reset because the end index needs to be adjusted
        return self

    def append_text_with_bold(self, text, value=True):
        text_style = {"bold": value}
        return self.append_text_with_style(text, text_style=text_style)

    def append_text_with_named_style(self, text, named_style):
        paragraph_style = {"named_style": named_style}
        return self.append_text_with_style(text, paragraph_style=paragraph_style)

    def append_text_with_style(self, text, text_style=None, paragraph_style=None):
        start_index = self.end_index
        self.append_text(text)
        end_index   = self.end_index
        range = { "start_index": start_index ,
                  "end_index"  : end_index   }
        if text_style:
            self.set_text_style_to_range(range, text_style)
        if paragraph_style:
            self.set_paragraph_style_to_range(range, paragraph_style)
        return self



    def background_color(self, color):
        text_style = {"background_color": color}
        #self.gdoc.add_request_text_style_to_range(self.range(), text_style)
        return self.set_text_style_to_range(self.range(), text_style)

    def clear(self):
        return self.set_text('\n')      # if we set it to an empty string, the named range will be deleted

    def info(self):
        return { "name"        : self.named_range_name,
                 "start_index" : self.start_index     ,
                 "end_index"   : self.end_index       }

    def insert_text(self, text):
        self.gdoc.insert_text(text=text, location=self.start_index)
        self.end_index += len(text)
        self.reset_named_range()            # need to reset because the start index needs to be adjusted
        return self

    def page_break(self):
        self.gdoc.add_request_page_break(self.end_index)
        return self

    def new_line(self):
        self.append_text('\n')
        return self

    def range(self):
        return {"start_index": self.start_index, "end_index": self.end_index}

    # bug: named_range is not correctly fixed when there are more than one match
    # todo: see if there is a way to detect the number of matches
    def replace(self, text_to_find, text_to_replace):
        self.gdoc.add_request_replace_text(text_to_find=text_to_find, text_to_replace=text_to_replace)
        self.end_index = self.end_index + len(text_to_replace) - len(text_to_find)
        #print(self.end_index)
        self.reset_named_range()
        return self

    def reset_named_range(self):
        self.gdoc.add_request_named_range_reset(name=self.named_range_name,start_index=self.start_index, end_index=self.end_index)
        return self

    def set_paragraph_style_to_range(self, range, paragraph_style):
        return self.gdoc.add_request_paragraph_style_to_range(range, paragraph_style)

    def set_range_indexes(self):
        ranges           = self.gdoc.named_range_ranges(self.named_range_name)
        data             = self.gdoc.ranges_start_and_end(ranges)
        self.start_index = data.get('start_index')
        self.end_index   = data.get('end_index')
        return self

    def set_text(self, text):
        if self.start_index:
            self.gdoc.add_request_replace_named_range_content(name=self.named_range_name, text=text)
            self.end_index = self.start_index + len(text)
        return self

    def set_text_style_to_range(self, range, text_style):
        return self.gdoc.add_request_text_style_to_range(range, text_style)

    def __repr__(self):
        info = self.info()
        return f"{info.get('name')} - from {info.get('start_index')} to {info.get('end_index')}"

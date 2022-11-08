import random

from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.testing.Duration import Duration


class Alignment:
    ALIGNMENT_UNSPECIFIED   = "ALIGNMENT_UNSPECIFIED"
    START                   = "START"
    CENTER                  = "CENTER"
    END                     = "END"
    JUSTIFIED               = "JUSTIFIED"


class Baseline_Offset:
    UNSPECIFIED = 'BASELINE_OFFSET_UNSPECIFIED'
    NONE        = 'NONE'
    SUPERSCRIPT = 'SUPERSCRIPT'
    SUBSCRIPT   = 'SUBSCRIPT'

class Direction:
    UNSPECIFIED   = "CONTENT_DIRECTION_UNSPECIFIED"
    LEFT_TO_RIGHT = "LEFT_TO_RIGHT"
    RIGHT_TO_LEFT = "RIGHT_TO_LEFT"

class RGB:                                                                  # see https://kierandixon.com/google-sheets-colors/ for list of colors
    AZURE       = { "red": 0      , "green": 0.5    , "blue": 1      }
    BLACK       = { "red": 0      , "green": 0      , "blue": 0      }
    BLUE        = { "red": 0      , "green": 0      , "blue": 1      }
    BLUE_L2     = { "red": 159/255, "green": 197/255, "blue": 232/255} # light blue 2  | 9fc5e8 | 159, 197, 232
    BLUE_L3     = { "red": 207/255, "green": 226/255, "blue": 243/255} # light blue 3  | cfe2f3 | 207, 226, 243
    CYAN        = { "red":   0/255, "green": 255/255, "blue": 255/255} # cyan          | 00ffff |   0, 255, 255
    CYAN_L1     = { "red": 118/255, "green": 165/255, "blue": 175/255} # light cyan  1 | 76a5af | 118, 165, 175
    CYAN_L2     = { "red": 162/255, "green": 196/255, "blue": 201/255} # light cyan  2 | a2c4c9 | 162, 196, 201
    CYAN_L3     = { "red": 208/255, "green": 224/255, "blue": 227/255} # light cyan  3 | d0e0e3 | 208, 224, 227
    #DARK_BLUE_2 = { "red": 0.04   , "green": 0.33   , "blue": 0.58   }
    GREEN       = { "red": 0      , "green": 1      , "blue": 0      }
    GREEN_L1    = { "red": 147/255, "green": 196/255, "blue": 125/255} # light green 1 | 93c47d | 147, 196, 125
    GREEN_L2    = { "red": 182/255, "green": 215/255, "blue": 168/255} # light green 2 | b6d7a8 | 182, 215, 168
    GREEN_L3    = { "red": 217/255, "green": 234/255, "blue": 211/255} # light green 3 | d9ead3 | 217, 234, 211
    GREY        = { "red": 204/255, "green": 204/255, "blue": 204/255} # grey          | ccccc  | 204, 204, 204
    GREY_L1     = { "red": 217/255, "green": 217/255, "blue": 217/255} # light grey  1 | d9d9d9 | 217, 217, 217
    GREY_L2     = { "red": 239/255, "green": 239/255, "blue": 239/255} # light grey  2 | efefef | 239, 239, 239
    GREY_L3     = { "red": 243/255, "green": 243/255, "blue": 243/255} # light grey  3 | f3f3f3 | 243, 243, 243
    GREY_D1     = { "red": 183/255, "green": 183/255, "blue": 183/255} # Dark grey  1  | b7b7b7 | 183, 183, 183
    GREY_D2     = { "red": 153/255, "green": 153/255, "blue": 153/255} # Dark grey  2  | 999999 | 153, 153, 153
    GREY_D3     = { "red": 102/255, "green": 102/255, "blue": 102/255} # Dark grey  3  | 666666 | 102, 102, 102
    GREY_D4     = { "red":  67/255, "green":  67/255, "blue":  67/255} # Dark grey  4  | 434343 |  67,  67,  67
    RED         = { "red": 1      , "green": 0      , "blue": 0      }
    RED_L3      = { "red": 244/255, "green": 204/255, "blue": 204/255} # light red 3   | f4cccc | 244, 204, 204
    WHITE       = { "red": 1      , "green": 1      , "blue": 1      }

    @cache_on_self
    def all_color_keys(self):
        return list(key for key, value in RGB.__dict__.items() if isinstance(value, dict))

    @cache_on_self
    def all_color_values(self):
        return list(value for key, value in RGB.__dict__.items() if isinstance(value, dict))

    def random_color_value(self):
        return random.choice(self.all_color_values())


        #return set(RGB)

class Border_Style:
    DOTTED	        = "DOTTED"
    DASHED          = "DASHED"
    SOLID           = "SOLID"
    SOLID_MEDIUM    = "SOLID_MEDIUM"
    SOLID_THICK     = "SOLID_THICK"
    NONE            = "NONE"
    DOUBLE          = "DOUBLE"

class Content_Alignment:
    UNSPECIFIED = "CONTENT_ALIGNMENT_UNSPECIFIED"
    TOP         = "TOP"
    MIDDLE      = "MIDDLE"
    BOTTOM      = "BOTTOM"

class Dash_Style:
    UNSPECIFIED = "DASH_STYLE_UNSPECIFIED"
    SOLID       = "SOLID"
    DOT         = "DOT"
    DASH        = "DASH"

class Font_Family:
    ARIAL           = "Arial"
    CAVEAT          = "Caveat"
    OSWALD          = "Oswald"
    VERDANA         = "Verdana"

class Merge_Type:
    MERGE_ALL     = "MERGE_ALL"
    MERGE_COLUMNS = "MERGE_COLUMNS"
    MERGE_ROWS    = "MERGE_ROWS"

class Named_Style:
    UNSPECIFIED = "NAMED_STYLE_TYPE_UNSPECIFIED"
    NORMAL_TEXT = "NORMAL_TEXT"
    TITLE	    = "TITLE"
    SUBTITLE    = "SUBTITLE"
    HEADING_1   = "HEADING_1"
    HEADING_2   = "HEADING_2"
    HEADING_3   = "HEADING_3"
    HEADING_4   = "HEADING_4"
    HEADING_5   = "HEADING_5"
    HEADING_6   = "HEADING_6"

class Spacing_Mode:
    SPACING_MODE_UNSPECIFIED = "SPACING_MODE_UNSPECIFIED"
    NEVER_COLLAPSE           = "NEVER_COLLAPSE"
    COLLAPSE_LISTS           = "COLLAPSE_LISTS"

class Width_Type:
    UNSPECIFIED            = "WIDTH_TYPE_UNSPECIFIED"
    EVENLY_DISTRIBUTED     = "EVENLY_DISTRIBUTED"
    FIXED_WIDTH            = "FIXED_WIDTH"

class Wrap_Strategy:
    OVERFLOW_CELL = "OVERFLOW_CELL"
    CLIP          = "CLIP"
    WRAP          = "WRAP"

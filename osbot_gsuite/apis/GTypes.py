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

class RGB:
    BLACK       = { "red": 0    , "green": 0    , "blue": 0    }
    BLUE        = { "red": 0    , "green": 0    , "blue": 1    }
    DARK_BLUE_2 = { "red": 0.04 , "green": 0.33 , "blue": 0.58 }
    GREEN       = { "red": 0    , "green": 1    , "blue": 0    }
    GRAY        = { "red": 0.9  , "green": 0.9  , "blue": 0.9  }
    RED         = { "red": 1    , "green": 0    , "blue": 0    }
    WHITE       = { "red": 1    , "green": 1    , "blue": 1    }

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

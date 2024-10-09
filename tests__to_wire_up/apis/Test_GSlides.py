from time import sleep
from unittest        import TestCase

from osbot_gsuite.apis.GDrive import GDrive
from osbot_gsuite.apis.GSlides import GSlides


class Test_GDrive(TestCase):
    def setUp(self):
        self.gslides = GSlides()
        self.gdrive  = GDrive()

    # helper methods

    def get_target_slide_id(self):
        file_id  = self.gdrive.find_by_name('GSlides API tests').get('id')
        slides   = self.gslides.slides(file_id)
        slide_id = slides.pop().get('objectId')
        return file_id, slide_id

    # tests for GDrive methods

    def test_ctor(self):
        service = self.gslides.service
        assert service._baseUrl == 'https://slides.googleapis.com/'

    def test_all_presentations(self):
        result = self.gslides.all_presentations()
        assert len(result) > 0

    def test_presentation_get(self):
        presentation_id = self.gslides.presentation_create('created via Unit tests')
        result = self.gslides.presentation(presentation_id)

        assert set(result) == { 'layouts'       , 'locale'    , 'masters', 'notesMaster', 'pageSize',
                                'presentationId', 'revisionId', 'slides' , 'title'                  }

        assert result.get('title') == 'created via Unit tests'

        self.gdrive.file_delete(presentation_id)
        assert self.gslides.presentation(presentation_id) is None

    def test_presentation_create(self):
        presentation_id = self.gslides.presentation_create('created via Unit tests')
        Dev.pprint(presentation_id)

    def test_slide_copy(self):
        file_id = self.gdrive.find_by_name('GSlides API tests').get('id')
        slide_id = 'g4b149a1e32_0_0'
        new_slide_id = 'slide_3'
        result = self.gslides.slide_copy(file_id,slide_id,new_slide_id)
        Dev.pprint(result)

    def test_slide_create(self):
        file_id = self.gdrive.find_by_name('GSlides API tests').get('id')
        new_slide_id = 'new_slide_id'
        self.gslides.slide_delete(file_id, new_slide_id)
        result = self.gslides.slide_create(file_id, 2, 'TITLE_AND_BODY', new_slide_id)
        assert result == new_slide_id
        self.gslides.slide_delete(file_id, new_slide_id)
        result = self.gslides.slide_create(file_id)
        self.gslides.slide_delete(file_id, result)

    def test_slide_elements(self):
        test_id = self.gdrive.find_by_name('GSlides API tests').get('id')
        elements = self.gslides.slide_elements(test_id, 1)
        assert len(elements) > 0

    def test_slides(self):
        test_id = self.gdrive.find_by_name('GSlides API tests').get('id')
        slides = self.gslides.slides(test_id)
        assert len(slides) > 0

    def test_element_set_text(self):
        file_id    = self.gdrive.find_by_name('GSlides API tests').get('id')
        slides     = self.gslides.slides(file_id)
        element_id = slides.pop().get('pageElements').pop().get('objectId') # last element of the last slide
        text       = 'new text.....changed....'
        result     = self.gslides.set_element_text(file_id,element_id,text)

        assert result.get('presentationId') == file_id


    def test_delete_element__all_temp_created(self):
        file_id  = self.gdrive.find_by_name('GSlides API tests').get('id')
        elements = self.gslides.slide_elements_indexed_by_id(file_id,1)
        for key,element in elements.items():
            #Dev.pprint(key)
            if 'textbox_' in key.lower():
                Dev.pprint(self.gslides.element_delete(file_id,key))



    def test_add_element_text(self):
        (file_id, slide_id) = self.get_target_slide_id()
        text    = Misc.random_string_and_numbers(6,'New Text Field - ')
        x_pos   = 50
        y_pos   = 250
        width   = 300
        height  = 50
        new_id = self.gslides.element_create_text(file_id, slide_id, text, x_pos, y_pos, width, height)

        self.gslides.element_set_text(file_id,new_id,'changed text')
        sleep(2)
        self.gslides.element_delete(file_id,new_id)

    def test_element_create_image(self):
        (file_id, slide_id) = self.get_target_slide_id()
        image_url = 'https://pbx-group-security.com/img/pbx-gs/pbx-gs-logo.png'
        shape_id  = self.gslides.element_create_image(file_id, slide_id,image_url, 100,100,300,300)
        sleep(3)
        self.gslides.element_delete(file_id, shape_id)

    def test_element_create_shape(self):
        (file_id, slide_id) = self.get_target_slide_id()
        def test_shape_creation(shape_type):
            shape_id  = self.gslides.element_create_shape(file_id, slide_id, shape_type,225,50,300,300)
            #properties = {"shapeBackgroundFill": {"solidFill": {"alpha": 0.6, "color": {"themeColor": "ACCENT5"}}}}
            #self.gslides.element_set_shape_properties(file_id, shape_id, properties)
            if shape_id:
                self.gslides.element_delete(file_id, shape_id)

        # enabling all 140 shapes below will cause an "Quota exceeded for quota group 'WriteGroup' and limit 'USER-100s" error

        shapes = [  #'TEXT_BOX','RECTANGLE','ROUND_RECTANGLE','ELLIPSE','ARC','BENT_ARROW','BENT_UP_ARROW','BEVEL',
                    #'BLOCK_ARC','BRACE_PAIR','BRACKET_PAIR','CAN','CHEVRON','CHORD','CLOUD','CORNER','CUBE',
                    #'CURVED_DOWN_ARROW','CURVED_LEFT_ARROW','CURVED_RIGHT_ARROW','CURVED_UP_ARROW','DECAGON',
                    #'DIAGONAL_STRIPE','DIAMOND','DODECAGON','DONUT','DOUBLE_WAVE','DOWN_ARROW','DOWN_ARROW_CALLOUT',
                    #'FOLDED_CORNER','FRAME','HALF_FRAME','HEART','HEPTAGON','HEXAGON','HOME_PLATE','HORIZONTAL_SCROLL',
                    #'IRREGULAR_SEAL_1','IRREGULAR_SEAL_2','LEFT_ARROW','LEFT_ARROW_CALLOUT','LEFT_BRACE','LEFT_BRACKET',
                    #'LEFT_RIGHT_ARROW','LEFT_RIGHT_ARROW_CALLOUT','LEFT_RIGHT_UP_ARROW','LEFT_UP_ARROW','LIGHTNING_BOLT',
                    #'MATH_DIVIDE','MATH_EQUAL','MATH_MINUS','MATH_MULTIPLY','MATH_NOT_EQUAL','MATH_PLUS','MOON',
                    #'NO_SMOKING','NOTCHED_RIGHT_ARROW','OCTAGON','PARALLELOGRAM','PENTAGON','PIE','PLAQUE','PLUS',
                    #'QUAD_ARROW','QUAD_ARROW_CALLOUT','RIBBON','RIBBON_2','RIGHT_ARROW','RIGHT_ARROW_CALLOUT',
                    #'RIGHT_BRACE','RIGHT_BRACKET','ROUND_1_RECTANGLE','ROUND_2_DIAGONAL_RECTANGLE','ROUND_2_SAME_RECTANGLE',
                    #'RIGHT_TRIANGLE','SMILEY_FACE','SNIP_1_RECTANGLE','SNIP_2_DIAGONAL_RECTANGLE','SNIP_2_SAME_RECTANGLE',
                    #'SNIP_ROUND_RECTANGLE','STAR_10','STAR_12','STAR_16','STAR_24','STAR_32','STAR_4','STAR_5','STAR_6',
                    #'STAR_7','STAR_8','STRIPED_RIGHT_ARROW','SUN','TRAPEZOID','TRIANGLE','UP_ARROW','UP_ARROW_CALLOUT',
                    'UP_DOWN_ARROW','UTURN_ARROW','VERTICAL_SCROLL','WAVE','WEDGE_ELLIPSE_CALLOUT','WEDGE_RECTANGLE_CALLOUT',
                    'WEDGE_ROUND_RECTANGLE_CALLOUT','FLOW_CHART_ALTERNATE_PROCESS','FLOW_CHART_COLLATE','FLOW_CHART_CONNECTOR',
                    'FLOW_CHART_DECISION','FLOW_CHART_DELAY','FLOW_CHART_DISPLAY','FLOW_CHART_DOCUMENT','FLOW_CHART_EXTRACT',
                    'FLOW_CHART_INPUT_OUTPUT','FLOW_CHART_INTERNAL_STORAGE','FLOW_CHART_MAGNETIC_DISK','FLOW_CHART_MAGNETIC_DRUM',
                    'FLOW_CHART_MAGNETIC_TAPE','FLOW_CHART_MANUAL_INPUT','FLOW_CHART_MANUAL_OPERATION','FLOW_CHART_MERGE',
                    'FLOW_CHART_MULTIDOCUMENT','FLOW_CHART_OFFLINE_STORAGE','FLOW_CHART_OFFPAGE_CONNECTOR','FLOW_CHART_ONLINE_STORAGE',
                    'FLOW_CHART_OR','FLOW_CHART_PREDEFINED_PROCESS','FLOW_CHART_PREPARATION','FLOW_CHART_PROCESS','FLOW_CHART_PUNCHED_CARD',
                    'FLOW_CHART_PUNCHED_TAPE','FLOW_CHART_SORT','FLOW_CHART_SUMMING_JUNCTION','FLOW_CHART_TERMINATOR','ARROW_EAST',
                    'ARROW_NORTH_EAST','ARROW_NORTH','SPEECH','STARBURST','TEARDROPELLIPSE_RIBBON','ELLIPSE_RIBBON_2','CLOUD_CALLOUT']
        for shape in shapes:
            test_shape_creation(shape)

    def test_element_create_table(self):
        (file_id, slide_id) = self.get_target_slide_id()
        table_id  = self.gslides.element_create_table(file_id, slide_id)

        # the deleteText command (below) was throwing an error (I think it might be caused by the fact that there is no data in the cell)
        requests = [#{ "deleteText": {   "objectId"      : table_id,
                    #                    "cellLocation"  : {  "rowIndex": 4, "columnIndex": 2   },
                    #                    "textRange"     : {"type": "ALL"                     }}},
                    { "insertText": {   "objectId"      : table_id,
                                        "cellLocation"  : {  "rowIndex": 0, "columnIndex": 0   },
                                        "text"          : "text added",
                                        "insertionIndex": 0                                   }},]
        self.gslides.execute_requests(file_id, requests)
        requests = [ { "updateTableCellProperties"  : {   "objectId": table_id,
                                                          "tableRange": { "location"  : { "rowIndex"   : 0, "columnIndex": 0},
                                                                          "rowSpan"   : 1 ,
                                                                          "columnSpan": 1 },
                                                          "tableCellProperties": { "tableCellBackgroundFill":  { "solidFill": { "color": {"rgbColor": {"red": 0.0,"green": 0.0, "blue": 0.0 }}}}},
                                                          "fields"             : "tableCellBackgroundFill.solidFill.color"}},
                     { "updateTextStyle"            : {    "objectId": table_id,
                                                           "cellLocation": { "rowIndex": 0, "columnIndex": 0},
                                                           "style": { "foregroundColor": {
                                                                      "opaqueColor": { "rgbColor": {"red": 0.5,"green": 1.0,"blue": 0.5}} },
                                                                      "bold": True,
                                                                      "fontFamily": "Cambria",
                                                                      "fontSize": { "magnitude": 38,"unit": "PT" }},
                                                          "textRange": { "type": "ALL"},
                                                          "fields": "foregroundColor,bold,fontFamily,fontSize" }}]
        self.gslides.execute_requests(file_id, requests)
        sleep(3)
        self.gslides.element_delete(file_id, table_id)

    def test_element_set_text_style(self):
        (file_id, slide_id) = self.get_target_slide_id()
        shape_id = self.gslides.element_create_text(file_id, slide_id,width=400)

        style = {  'bold'            : True,
                   'italic'          : True,
                   'fontFamily'      : 'Times New Roman',
                   'fontSize'        : { 'magnitude'  : 74, 'unit': 'PT' },
                   'foregroundColor' : { 'opaqueColor': { 'rgbColor': { 'blue': 0.49803922, 'green': 1.0, 'red': 0.0 }}},
                    'link'           : { 'url': 'https://news.bbc.co.uk'         } }
        fields   = 'bold,italic,fontFamily,fontSize, foregroundColor,link'

        self.gslides.element_set_text_style(file_id,shape_id, style, fields)
        sleep(3)
        self.gslides.element_delete(file_id,shape_id)

    def test_element_set_shape_properties(self):
        (file_id, slide_id) = self.get_target_slide_id()
        shape_id = self.gslides.element_create_text(file_id, slide_id,width=400)

        properties = { "shapeBackgroundFill": { "solidFill"  : { "alpha": 0.6, "color": { "themeColor": "ACCENT5" } } },
                        "outline"           : { "dashStyle"  : "SOLID",
                                                "outlineFill": { "solidFill": { "alpha": 1, "color": { "themeColor": "ACCENT5" }} },
                                                "weight"     : {"magnitude": 3, "unit": "PT"                                    } },
                        "contentAlignment"  : 'MIDDLE'                                                                            }

        fields = "shapeBackgroundFill,outline, contentAlignment"

        self.gslides.element_set_shape_properties(file_id,shape_id,properties,fields)
        sleep(3)
        self.gslides.element_delete(file_id, shape_id)

    def test_element_set_via_requests(self):
        (file_id, slide_id) = self.get_target_slide_id()
        shape_id = self.gslides.element_create_text(file_id, slide_id, width=400)
        requests = []
        requests.append  ({ 'updateTextStyle'       : { 'objectId'       : shape_id  ,
                                                        'style'          : { 'fontSize': {'magnitude': 74, 'unit': 'PT'}},
                                                        'fields'         : 'fontSize'                                  }})
        requests.append  ({ 'updateParagraphStyle'  : { "objectId"       : shape_id,
                                                        "style"          : { "alignment": "CENTER" },
                                                        "fields"         : 'alignment'                                 }})
        requests.append  ({ "updateShapeProperties" : { "objectId"       : shape_id,
                                                        'shapeProperties': { "shapeBackgroundFill" : { "solidFill"  : { "alpha": 0.6, "color": { "themeColor": "ACCENT5" } } }},
                                                        'fields'         : 'shapeBackgroundFill'                       }})

        self.gslides.execute_requests(file_id, requests)
        sleep(2)
        self.gslides.element_delete(file_id, shape_id)
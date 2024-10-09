from osbot_gsuite.gsuite.drive.GDrive import GDrive
from osbot_utils.base_classes.Type_Safe import Type_Safe

from osbot_utils.utils import Misc


class GSlides(Type_Safe):
    presentations : object
    gdrive        : GDrive

    # def __init__(self, gsuite_secret_id=None):
    #     self.presentations = GSuite(gsuite_secret_id).slides_v1().presentations()
    #     self.gdrive        = GDrive(gsuite_secret_id)

    # misc utils

    def batch_update(self, file_id, requests):
        body = {'requests': requests}
        return self.execute(self.presentations.batchUpdate(presentationId=file_id, body=body))

    def execute(self,command):
        return self.gdrive.execute(command)

    def execute_requests(self, file_id, requests):
        return self.batch_update(file_id, requests)


    def random_id(self, prefix):
        return Misc.random_string_and_numbers(6, prefix + "_")


    def all_presentations(self):
        mime_type_presentations = 'application/vnd.google-apps.presentation'
        return self.gdrive.find_by_mime_type(mime_type_presentations)


    # Elements
    def element_create_image_request(self, page_id, image_url, x_pos=200, y_pos=200, width=100, height=100):
        return {  "createImage": {
                  "url"        : image_url,
                  "elementProperties": {
                      "pageObjectId": page_id,
                      "size": { "width" : { "magnitude": width, "unit": "PT" },
                                "height": { "magnitude": height,"unit": "PT" }},
                      "transform": { "scaleX": 1, "scaleY": 1, "translateX": x_pos, "translateY": y_pos, "unit": "PT" }}}}

    def element_create_image(self, file_id, page_id, image_url, x_pos=200, y_pos=200, width=100, height=100):
        requests = [ self.element_create_image_request(page_id, image_url, x_pos, y_pos, width, height)]
        result = self.batch_update(file_id, requests)
        if result:
            result_replies = result.get('replies')
            if result_replies:
                return result_replies[0].get('createImage').get('objectId')

    def element_create_table_request(self, slide_id, rows=3, cols=3, x_pos=200, y_pos=200, width=100, height=100, objectId=None):
        return { "createTable": { "objectId"         : objectId,
                                  "elementProperties": { "pageObjectId": slide_id,
                                                         "size"        : {  "width": {"magnitude":  width, "unit": "PT"},
                                                                            "height": {"magnitude": height,"unit": "PT"}},
                                                         "transform"   : { "scaleX": 1, "scaleY": 1, "translateX": x_pos, "translateY": y_pos,"unit": "PT" }},
                                  "rows"             : rows                         ,
                                  "columns"          : cols                        }}
                                  #"tableRows"        : [{'rowHeight':{ 'magnitude': 10, 'unit': 'PT'}},{'rowHeight':{ 'magnitude': 100, 'unit': 'PT'}}]}}
    def element_create_table(self, file_id, slide_id, rows=3, cols=3, x_pos=200, y_pos=200, width=100, height=100, objectId=None):
        requests = [  self.element_create_table_request(slide_id, rows, cols, x_pos, y_pos, width, height, objectId) ]
        result = self.batch_update(file_id, requests)
        if result:
            return result.get('replies')[0].get('createTable').get('objectId')

    def element_create_shape_request(self, page_id, x_pos=200, y_pos=200, width=100, height=100, objectId=None):
        return { 'createShape': { 'objectId': objectId,
                                  'shapeType': 'TEXT_BOX',
                                  'elementProperties': {
                                      'pageObjectId': page_id,
                                      'size'        : { 'height': { 'magnitude': height, 'unit': 'PT'},
                                                        'width' : { 'magnitude': width , 'unit': 'PT'}},
                                      'transform'   : { 'scaleX': 1, 'scaleY': 1, 'translateX': x_pos, 'translateY': y_pos, 'unit': 'PT' }}}}

    def element_create_text_requests(self, page_id, text = "Text...", x_pos=200, y_pos=200, width=100, height=100, objectId=None):
        return [ self.element_create_shape_request(page_id, x_pos, y_pos, width, height, objectId),
                 self.element_insert_text_request(objectId,text)]

    def element_create_text(self,file_id, page_id, text = "Text...", x_pos=200, y_pos=200, width=100, height=100, objectId=None):
        requests = self.element_create_text_requests(page_id, text, x_pos, y_pos, width, height, objectId)
        result = self.batch_update(file_id, requests)
        if result:
            return result.get('replies')[0].get('createShape').get('objectId')

    def element_create_shape(self,file_id, page_id, shape_type, x_pos=200, y_pos=200, width=100, height=100):
        requests = [ { 'createShape': { 'shapeType': shape_type,
                                        'elementProperties': {
                                            'pageObjectId': page_id,
                                            'size'        : { 'height': { 'magnitude': height, 'unit': 'PT'},
                                                              'width' : { 'magnitude': width , 'unit': 'PT'}},
                                            'transform'   : { 'scaleX': 1, 'scaleY': 1, 'translateX': x_pos, 'translateY': y_pos, 'unit': 'PT' }}}}]

        result = self.batch_update(file_id, requests)
        if result:
            return result.get('replies')[0].get('createShape').get('objectId')

    def element_delete(self, file_id, element_id):
        requests = [ {  'deleteObject' : { 'objectId': element_id } } ]
        return self.batch_update(file_id, requests)

    def element_insert_text_request(self, objectId, text):
        return { 'insertText': { 'objectId': objectId, 'insertionIndex': 0, 'text': text }}

    def element_set_table_cell_size_bold_requests(self, table_id, row, col, size, bold):
        style = {"bold": bold, "fontSize": { "magnitude": size, "unit": "PT" }}
        fields = "bold,fontSize"
        return self.element_set_table_text_style_request(table_id, row,col,style,fields)

    def element_set_table_text_style_request(self, shape_id, row, col,style, fields):
        return {'updateTextStyle': { 'objectId'    : shape_id  ,
                                     "cellLocation": {"rowIndex": row, "columnIndex": col},
                                     'style'       : style     ,
                                     'fields'      : fields   }}

    def element_set_table_text_requests(self, table_id, row, col, text):
        return     [#{ "deleteText": {   "objectId"      : table_id,
                    #                    "cellLocation"  : {  "rowIndex": row, "columnIndex": col   },
                    #                    "textRange"     : {"type": "ALL"                         }}},
                    { "insertText": {   "objectId"      : table_id,
                                        "cellLocation"  : {  "rowIndex": row, "columnIndex": col   },
                                        "text"          : text,
                                        "insertionIndex": 0                                       }}]

    def element_set_table_text(self, file_id, table_id, row, col, text):
        requests = self.element_set_table_text_requests(table_id, row, col, text)

        self.execute_requests(file_id,requests)


    def element_set_table_column_width_request(self,table_id, column_index, column_width):

        return { 'updateTableColumnProperties': { 'objectId': table_id, "columnIndices": [column_index],
                                                  "tableColumnProperties": { 'columnWidth': { "magnitude": column_width, "unit": "PT" } },
                                                  "fields": "columnWidth" } }

    def element_set_table_cell_aligment_request(self, table_id, row_index, column_index, row_span, column_span, alignment='MIDDLE'):
        return { "updateTableCellProperties": { "objectId": table_id,
                                                "tableRange": {
                                                    "location": { "rowIndex":  row_index,"columnIndex": column_index },
                                                                  "rowSpan": row_span, "columnSpan": column_span },
                                                "tableCellProperties": { "contentAlignment": alignment },
                                                "fields": "contentAlignment"}}

    def element_set_table_row_height_request(self, table_id, height):
        return  { "updateTableRowProperties": {   "objectId": table_id,
                                                  "rowIndices": 0,
                                                  "tableRowProperties": { "minRowHeight":  { 'magnitude': height, 'unit': 'PT'}},
                                                  "fields"            : "minRowHeight"}}

    def element_set_text_requests(self, file_id, element_id, text):
        return [ {   'deleteText' : { 'objectId'      : element_id         ,
                                      'textRange'     : { 'type': 'ALL' }}},
                 {
                     'insertText': { 'objectId'      : element_id          ,
                                     'insertionIndex': 0                   ,
                                     'text'          : text              }}]
    def element_set_text(self, file_id, element_id, text):

        requests =  self.element_set_text_requests(file_id, element_id, text)

        return self.batch_update(file_id, requests)

    def element_set_text_style_requests(self, object_id, style, fields):
        return {'updateTextStyle': { 'objectId': object_id  ,
                                     'style'   : style     ,
                                     'fields'  : fields   }}

    def element_set_text_style(self, file_id, shape_id,style, fields):
        requests = [ self.element_set_text_style_requests(shape_id, style, fields) ]
        return self.batch_update(file_id, requests)


    def element_set_text_style_requests__for_title(self, shape_id, font_size, blue=0.5, green=0.5, red=0.5):
        style = {  'bold'            : True,
                   'fontFamily'      : 'Avenir',
                   'fontSize'        : { 'magnitude'  : font_size, 'unit': 'PT' },
                   'foregroundColor' : {'opaqueColor': {'rgbColor': {'blue': blue, 'green': green, 'red': red}}}}
        fields   = 'bold,fontFamily,fontSize,foregroundColor'


        return self.element_set_text_style_requests(shape_id, style, fields)

    def element_set_shape_properties(self, file_id, shape_id,properties , fields=None):
        if fields is None:
            fields = ",".join(list(set(properties)))
        requests = [{'updateShapeProperties': { 'objectId'         : shape_id     ,
                                                'shapeProperties'  : properties   ,
                                                'fields'           : fields     }}]
        return self.batch_update(file_id, requests)

    def presentation_create(self, title):
        body = { 'title': title }
        presentation = self.presentations.create(body=body).execute()
        return presentation.get('presentationId')

    def presentation_copy(self, file_id, title, parent_folder):
        body  = { 'name': title, 'parents':[parent_folder] }
        result = self.execute(self.gdrive.files.copy(fileId = file_id, body=body))
        return result.get('id')

    def presentation_metadata(self,presentation_id):
        try:
            return self.presentations.get(presentationId = presentation_id).execute()
        except:
            return None

    def slide_delete_request(self, slide_id):
        return { "deleteObject": { "objectId" : slide_id}}

    def slide_delete(self, presentation_id, slide_id):
        requests =   [ self.slide_delete_request(slide_id) ]
        return self.execute_requests(presentation_id, requests)

    def slide_copy(self,presentation_id, slide_id, new_slide_id, objects_ids = {}):
        requests =   [ { "duplicateObject": {
                                                "objectId" : slide_id,
                                                "objectIds": objects_ids}} ]
        requests[0]['duplicateObject']['objectIds'][slide_id] = new_slide_id
        return self.execute_requests(presentation_id, requests)

    def slide_create_request(self, new_slide_id=None, layout='BLANK' , insert_at= None ):
        return { "createSlide": {       "objectId"      : new_slide_id,
                                        'insertionIndex': insert_at,
                                        'slideLayoutReference': { 'predefinedLayout': layout } }}

    def slide_create(self, presentation_id, insert_at=1, layout='TITLE', new_slide_id=None):
        requests =   [ self.slide_create_request(new_slide_id, layout, insert_at)]
        result = self.execute_requests(presentation_id, requests)
        if result:
            return result.get('replies')[0].get('createSlide').get('objectId')


    def slide_move_to_pos_request(self, presentation_id, slide_id, pos):
        return [{ "updateSlidesPosition": { "slideObjectIds": [ slide_id],
                                            "insertionIndex": pos }}]
    def slide_move_to_pos(self, presentation_id, slide_id, pos):
        requests = self.slide_move_to_pos_request(presentation_id, slide_id, pos)
        return self.execute_requests(presentation_id,requests)

    def slide_elements(self, presentation_id, page_number):
        slides = self.slides(presentation_id)
        page   = slides[page_number]
        if page:
            return page.get('pageElements')
        return []

    def slide_elements_via_id(self, presentation_id, slide_id):
        slides = self.slides_indexed_by_id(presentation_id)
        slide = slides.get(slide_id)
        if slide:
            return slide.get('pageElements')
        return []

    def slide_elements_via_id_indexed_by_id(self, presentation_id, slide_id):
        elements = {}
        for element in self.slide_elements_via_id(presentation_id,slide_id):
            elements[element.get('objectId')] = element
        return elements

    def slides(self, presentation_id):
        presentation = self.presentation_metadata(presentation_id)
        if presentation:
            return presentation.get('slides')
        return []

    def slides_indexed_by_id(self, presentation_id):
        presentation = self.presentation_metadata(presentation_id)
        slides = {}
        if presentation:
            for slide in presentation.get('slides'):
                slides[slide.get('objectId')] = slide
        return slides



    # Helper methods

    def add_slide_with_table_from_array(self, file_id, slide_id, title, data, row_widths = []):
        title_id  = '{0}_title'.format(slide_id)
        table_id  = '{0}_table'.format(slide_id)
        headers   = data.pop(0)
        cols      = len(headers)
        rows      = len(data) + 1
        cell_size = 7
        self.slide_delete(file_id, slide_id)
        requests = [ self.slide_create_request                      (slide_id                           ),
                     self.element_create_shape_request              (slide_id, 10, 10, 500, 50, title_id),
                     self.element_insert_text_request               (title_id, title),
                     self.element_set_text_style_requests__for_title(title_id, 26),
                     self.element_create_table_request              (slide_id, rows, cols, 12, 80, 700, 270, table_id),
                     #self.element_set_table_row_height_request      (table_id, 10)
                    ]

        for col_index, header in enumerate(headers):
            requests.extend(self.element_set_table_text_requests          (table_id, 0,col_index, header  ))
            requests.append(self.element_set_table_cell_size_bold_requests(table_id, 0,col_index, 11, True))

        for row_index, row in enumerate(data):
            for col_index, cell in enumerate(row):
                requests.extend(self.element_set_table_text_requests(table_id          , row_index + 1, col_index, cell))
                requests.append(self.element_set_table_cell_size_bold_requests(table_id, row_index + 1, col_index, cell_size, False))

        for index, row_width in enumerate(row_widths):
            requests.append(self.element_set_table_column_width_request(table_id, index, row_width))

        requests.append(self.element_set_table_cell_aligment_request(table_id, 0,0, rows,cols))

        self.execute_requests(file_id, requests)
        return table_id

    def add_slide_with_table_from_object(self, file_id, slide_id, title, data):

        title_id = '{0}_title'.format(slide_id)
        table_id = '{0}_table'.format(slide_id)
        headers  = list(set(data))
        rows     = len(headers)                        # number of fields to show
        cols     = 2                                   # name:value pair
        requests = [ self.slide_create_request(slide_id),
                     self.element_create_shape_request              (slide_id, 10, 10, 500,  50, title_id                ),
                     self.element_insert_text_request               (title_id,title                                      ),
                     self.element_set_text_style_requests__for_title(title_id, 26                                        ),
                     self.element_create_table_request              (slide_id, rows , cols, 12, 80, 700, 270, table_id   ),
                     self.element_set_table_column_width_request    (table_id, 0 ,110                                    ),
                     self.element_set_table_column_width_request    (table_id, 1, 585                                    )]

        for index, header in enumerate(headers):
           requests.extend(self.element_set_table_text_requests          (table_id, index, 0, header))
           requests.extend(self.element_set_table_text_requests          (table_id, index, 1, str(data[header])))
           requests.append(self.element_set_table_cell_size_bold_requests(table_id, index, 0, 10, True))
           requests.append(self.element_set_table_cell_size_bold_requests(table_id, index, 1, 9 , False))

        #requests.extend(self.element_set_table_text_requests        (table_id, 1, 0, headers.pop()))

        self.execute_requests(file_id, requests)

        #requests = [self.element_set_table_text_requests(table_id, 1, 1, 'headers.pop()')]

        #self.execute_requests(file_id, requests)
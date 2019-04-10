import sys ; sys.path.append('..')

import unittest
from unittest import TestCase

from pbx_gs_python_utils.utils.Dev                  import Dev
from gsbot_gsuite.apis.create_slides.Project_Slides import Project_Slides


@unittest.skip('review and move long running into separate class')
class Test_Project_Slides(TestCase):
    def setUp(self):
        #self.jira_key       = 'GSSP-236'
        self.jira_key       = 'GSSP-149'
        #self.jira_key       = 'GSSP-49' # access control review
        #self.jira_key       = 'GSSP-241' # Ask Jody
        self.project_slides = Project_Slides().resolve_file_id(self.jira_key)

    def test_get_file_id(self):
        file_id  = self.project_slides.resolve_file_id(self.jira_key).file_id
        assert file_id == '1LZfAKrHWA6RHL7s9_7LzUV7h395bSj6WgCtCgFwsb-0'
        assert self.project_slides.gdrive().file_weblink(file_id) == 'https://drive.google.com/open?id=1LZfAKrHWA6RHL7s9_7LzUV7h395bSj6WgCtCgFwsb-0'

    @unittest.skip
    def test_delete_presentation(self):
        (self.project_slides.resolve_file_id(self.jira_key)
             .delete_presentation())

    def test_delete_all_content_slides(self):
        self.project_slides.delete_all_content_slides()

    def test_set_content_title_slide(self):
        (self.project_slides.resolve_file_id(self.jira_key)
                            .set_content_title_slide())
        #Dev.pprint(self.project_slides.gdrive().file_weblink(self.project_slides.file_id))

    def test_add_slide_project_details(self): self.project_slides.add_slide_project_details()
    def test_add_slide_services_used  (self): self.project_slides.add_slide_services_used()

    def test_add_slide_with_graph_all_1(self)       : self.project_slides.add_slide_with_graph_all_1       ()
    def test_add_slide_with_project_1_pager(self)   :
        self.project_slides.add_slide_with_project_1_pager('GSSP-127')# , 'GSSP-111')('GSSP-243')

        #self.project_slides.add_slides_with_project_1_pager(['GSSP-127','GSSP-111', 'GSSP-243'])

    def test_add_slide_with_graph_risks_to_R1 (self): self.project_slides.add_slide_with_graph_risks_to_R1 ()
    def test_add_slide_with_graph_stakeholders(self): self.project_slides.add_slide_with_graph_stakeholders()

    def test_add_slide_risks_reduced(self):
        self.project_slides.add_slide_risks_reduced()

    def test_add_metadata_slide(self):
        self.project_slides.resolve_file_id(self.jira_key)
        self.project_slides.add_metadata_slide()

    def test_add_slide_with_issues_linked(self):
        #self.project_slides.resolve_file_id('IA-404').set_jira_key('IA-408')
        #self.project_slides.add_slide_with_issues_linked('is parent of', "Services")
        self.project_slides.resolve_file_id('IA-404').set_jira_key('GSSP-115')
        self.project_slides.add_slide_with_issues_linked('delivered by', "Projects")
        Dev.pprint(self.project_slides.gdrive().file_weblink(self.project_slides.file_id))

    def test_project(self):
        Dev.pprint(self.project_slides.project())

    def test_create_slides_text_content(self):
        #self.project_slides.delete_presentation(self.jira_key)
        result = self.project_slides.create_slides_text_content(self.jira_key)
        Dev.pprint(result)

    def test_create_slides_graphs(self):
        self.project_slides.create_slides_graphs()

    # helper methods

    # def test_update_lambda(self):
    #     Lambda('gs.lambda_slides').update_with_src()


    def test_change_table_format(self):
        table_id = 'content_first_graph_table'

        requests = [ self.project_slides.gslides().element_set_table_cell_size_bold_requests(table_id, 0,0,10, False)]

            # {"updateTextStyle": {"objectId": table_id,
            #                      "cellLocation": {"rowIndex": 0, "columnIndex": 1},
            #                      "style": {"foregroundColor": {
            #                          "opaqueColor": {"rgbColor": {"red": 0.5, "green": 1.0, "blue": 0.5}}},
            #                          "bold": True,
            #                          "fontFamily": "Cambria",
            #                          "fontSize": {"magnitude": 38, "unit": "PT"}},
            #                      "textRange": {"type": "ALL"},
            #                      "fields": "foregroundColor,bold,fontFamily,fontSize"}}]


        file_id = self.project_slides.resolve_file_id(self.jira_key).file_id
        self.project_slides.gslides().execute_requests(file_id, requests)

    def test_fix_title_slide_id(self):
        #file_id = '1oApT1ujAcPuw_zMk8O5fVew9Mo4xNA28VHdLoq5DfX0'
        file_id = self.project_slides.resolve_file_id(self.jira_key).file_id
        gslides = self.project_slides.gslides()
        #gslides.slide_copy(template_file_id, 'g4ee1fc8bdc_0_0','slide_title')
        #Dev.pprint(set(gslides.slides_indexed_by_id(file_id)))
        Dev.pprint(gslides.slide_elements_via_id_indexed_by_id(file_id, 'content_first_graph'))

        # gslides.slide_copy(file_id, 'new_slide_title', 'slide_title',
        #                             { 'slide_title____title'      : 'slide_title___subtitle' ,
        #                               'slide_title____subtitle'   : 'slide_title___title' })

        #Dev.pprint(set(gslides.slide_elements_via_id_indexed_by_id(file_id, 'slide_title')))

        #gslides.element_set_text(file_id, 'slide_title___title', 'title')
        #gslides.element_set_text(file_id, 'slide_title___subtitle' ,'subtitle')

# Function slides (to move to separate File)
@unittest.skip('review and move long running into separate class')
class Test_Function_Slides(TestCase):
    def setUp(self):
        # self.jira_key       = 'GSSP-236'
        # self.jira_key       = 'GSSP-149'
        # self.jira_key       = 'GSSP-49' # access control review
        #self.jira_key = 'GSSP-241'  # Ask Jody
        self.project_slides = Project_Slides()


    def test_create_slides_for_function(self):
        key ='IA-407'  # Educate
        key = 'IA-404'  # Detect
        #key = 'IA-425'
        result = self.project_slides.create_slides_for_function(key)

        Dev.pprint(result)

    def test_create_project_slides_for_function(self):
        key = 'IA-407'  # Educate
        key = 'GSSP-112'  # Detect
        # key = 'IA-425'
        result = self.project_slides.create_project_slides_for_functions(key,None,None)

        Dev.pprint(result)


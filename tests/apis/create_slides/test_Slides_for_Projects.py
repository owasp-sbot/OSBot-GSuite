import sys
sys.path.append('..')
import unittest
from   unittest import TestCase

from osbot_gsuite.apis.create_slides.Slides_for_Projects import Slides_for_Projects
from pbx_gs_python_utils.utils.Dev          import Dev
from pbx_gs_python_utils.utils.Misc         import Misc

@unittest.skip('review and move long running into separate class')
class test_Slides_For_Projects(TestCase):

    def setUp(self):
        self.slides_for_projects = Slides_for_Projects()
        self.file_id             = self.slides_for_projects.file_id
        self.project_id          = 'GSSP-128' #'GSSP-232' #
        self.slide_id            = 'project-GSSP-128'
        self.title_id            = '{0}_title'.format(self.slide_id)

    def test_create_slide(self):
        slide_to_copy_id = 'g4cb8e4f3f7_0_0'
        new_slide_id     = self.slide_id
        object_ids       = { self.title_id : 'an_title_id'}
        self.slides_for_projects.create_slide(slide_to_copy_id, new_slide_id, object_ids)

    def test_create_slide_with_one_graph(self):
        graph_1 = ('GSSP-116','2', 'delivered by')
        self.slides_for_projects.create_slide_with_one_graph('graphs_gs_projects','Detect Projects',graph_1)

    def test_gs_project(self):
        title = 'Centralised AWS  Logging'
        assert self.slides_for_projects.gs_project(title).get('Key') == 'GSSP-128'
        assert self.slides_for_projects.gs_project("aaa")            is None

    def test_gs_projects(self):
        assert len(    self.slides_for_projects.gs_projects()          ) > 100
        assert len(set(self.slides_for_projects.gs_projects_by_id()   )) > 100
        assert len(set(self.slides_for_projects.gs_projects_by_title())) > 100
        Dev.pprint(self.slides_for_projects.gs_projects_by_title())

    def test_gs_services(self):
        Dev.pprint(self.slides_for_projects.gs_services())
        #assert len(    self.slides_for_projects.gs_projects()          ) > 100

    def test_get_slide(self):
        slide = self.slides_for_projects.get_slide(self.slide_id)
        Dev.pprint(slide)

    def test_set_slide_title(self):
        title = Misc.random_string_and_numbers(10, self.project_id + "  -  ")
        self.slides_for_projects.set_slide_title_request(self.slide_id, title)

        elements = self.slides_for_projects.gslides().slide_elements_via_id_indexed_by_id(self.file_id,self.slide_id)

        assert elements[self.title_id].get('shape').get('text')          \
                                          .get('textElements')[1]        \
                                          .get('textRun')                \
                                          .get('content').strip() == title

    def test_set_slide_link(self):
        self.slides_for_projects.set_slide_link(self.slide_id, self.project_id  )

    def test_set_table_text(self):
        text = 'CCC new text'
        self.slides_for_projects.set_table_text(self.slide_id, 0,0, text)

    def test_create_slide_with_project_data(self):
        self.slides_for_projects.create_slide_with_project_data(self.project_id)

    def test_create_slides_with_graphs(self):
        self.slides_for_projects.create_slides_with_graphs(self.project_id)

    def test_create_slides_with_projects_and_services(self):
        projects_key  = 'GSSP-116'
        services_key  = 'IA-418'
        function_name = 'Detect'
        self.slides_for_projects.create_slides_with_projects_and_services(function_name, projects_key, services_key)

    def test_create_slides_for_function___Cloud(self):
        self.slides_for_projects.create_slides_for_function___Cloud()

    def test_create_slides_for_project(self):
        key = 'GSSP-236'
        result = self.slides_for_projects.create_slides_for_project(key)

        Dev.pprint(result)









    # helper tests
    def test____view_master_elements(self):
        slide_id = 'g4ecf9bad4f_0_0' #self.slides_for_projects.master_slide
        #data = self.slides_for_projects.gslides().slide_elements_via_id_indexed_by_id(self.file_id,slide_id)
        data = self.slides_for_projects.gslides().slides_indexed_by_id(self.file_id)

        Dev.pprint(set(data))

        Dev.pprint(self.slides_for_projects.set_slides_positions(['GSSP-47','GSSP-128']))









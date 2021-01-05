from osbot_elastic.Elastic_Search import Elastic_Search

from osbot_gsuite.apis.GDrive                           import GDrive
from osbot_gsuite.apis.GSheets                          import GSheets
from osbot_gsuite.apis.GSlides                          import GSlides
from osbot_gsuite.apis.create_slides.GSBot_Helpers      import GSBot_Helper
from osbot_gsuite.apis.create_slides.GSBot_to_GDrive    import GSBot_to_GDrive



class Slides_for_Projects:
    def __init__(self, gsuite_secret_id=None):
        self.file_id                = '1mmDcM4JzrYvLjVd2werl1jXhEaCRlksCSRpocGRI0H4'
        self.index                  = 'it_assets,jira'
        self.secret_id              = 'elastic-jira-dev-2'
        self.gsuite_secret_id       = gsuite_secret_id
        self.master_slide           = 'g4cb8e4f3f7_0_0'
        self.master_title_id        = 'g4cb8e4f3f7_0_3'
        self.master_link_id         = 'g4eced7afc3_1_0'
        self.master_table_id        = 'g4cb8e4f3f7_0_2'
        self.master_graphs_slide_id = 'g4ecf9bad4f_0_0'
        self.master_graphs_title_id = 'g4ecf9bad4f_0_3'
        self.master_graphs_table_id = 'g4ecf9bad4f_0_2'
        self.jira_link              = 'https://jira.photobox.com/browse/{0}'
        self._elastic               = None
        self._gslides               = None
        self._gdrive                = None
        self._gsheets               = None

    def add_graph_to_slide(self, slide_id,graph_name_or_key, depth,links_path,x,y,width,height):
        gsuite_secret_id = 'gsuite_gsbot_user'          # to refactor
        gsbot_helper     = GSBot_Helper()
        gsbot_to_GDrive  = GSBot_to_GDrive(gsuite_secret_id)
        png_file         = gsbot_helper.get_png_from_expanded_graph(graph_name_or_key, depth,links_path)
        image_id         = gsbot_to_GDrive.upload_png_file_to_gdrive(png_file)

        image_url = "https://lh3.google.com/u/1/d/{0}".format(image_id)

        return self.gslides().element_create_image(self.file_id, slide_id, image_url, x, y, width, height)


    def create_slide(self, slide_to_copy_id, new_slide_id, object_ids = {}):
        #slides = self.gslides().slides_indexed_by_id(self.file_id)
        return self.gslides().slide_copy(self.file_id, slide_to_copy_id, new_slide_id,object_ids)

    def create_slide_with_one_graph(self,slide_id, title, graph_1):
        title_id = '{0}_title'.format(slide_id)
        table_id = '{0}_table'.format(slide_id)
        object_ids               = {
                                        self.master_graphs_title_id : title_id,
                                        self.master_graphs_table_id : table_id
                                   }
        self.gslides().slide_delete(self.file_id, slide_id)
        self.create_slide(self.master_graphs_slide_id, slide_id, object_ids)
        self.gslides().element_set_text(self.file_id, title_id, title)
        self.gslides().element_delete(self.file_id, table_id)

        self.add_graph_to_slide(slide_id, graph_1[0], graph_1[1], graph_1[2], 50, 60, 500, 300)

    def create_slide_with_two_graphs(self, slide_id, title, graph_1=None, graph_2=None):
        title_id                 = '{0}_title'.format(slide_id)
        table_id                 = '{0}_table'.format(slide_id)
        object_ids               = {
                                        self.master_graphs_title_id : title_id ,
                                        self.master_graphs_table_id : table_id
                                   }
        self.gslides().slide_delete(self.file_id,slide_id)
        self.create_slide(self.master_graphs_slide_id,slide_id, object_ids)
        #title                    = "Graphs - Risks and Stakeholders"
        self.gslides().element_set_text(self.file_id, title_id, title)
        #self.slides_for_projects.add_graph_to_slide(slide_id, 'GSSP-128','7','affects,stakeholders_up'      , 120, 200, 500, 200)
        if graph_1:
            self.gslides().element_set_table_text(self.file_id, table_id, 0,0, graph_1[0])
            self.add_graph_to_slide(slide_id, graph_1[1], graph_1[2], graph_1[3], 120, 60, 500, 130)
        if graph_2:
            self.gslides().element_set_table_text(self.file_id, table_id, 1, 0, graph_2[0])
            self.add_graph_to_slide(slide_id, graph_2[1], graph_2[2], graph_2[3], 130, 220, 500, 130)

    def elastic(self):
        if self._elastic is None:
            self._elastic = Elastic_Search()._setup_Elastic_on_cloud_via_AWS_Secret(self.index, self.secret_id)
        return self._elastic

    def get_slide(self, slide_id):
        #slides = self.gslides().slides_indexed_by_id(self.file_id)  # get all slides
        #slide  = slides.get(slide_id)                               # search for slide
        #if slide:                                                   # return if it exists already
        #    return slide
        self.gslides().slide_delete(self.file_id,slide_id)
        object_ids = {
                        self.master_title_id : '{0}_title'.format(slide_id),
                        self.master_link_id  : '{0}_link' .format(slide_id),
                        self.master_table_id : '{0}_table'.format(slide_id)
                        }
        self.create_slide(self.master_slide, slide_id,object_ids)   # create slide
        return self.gslides().slides_indexed_by_id(self.file_id)    # get slide data

    def gslides(self):
        if self._gslides is None:
            self._gslides = GSlides(self.gsuite_secret_id)
        return self._gslides

    def gdrive(self):
        if self._gdrive is None:
            self._gdrive = GDrive(self.gsuite_secret_id)
        return self._gdrive

    def gsheets(self):
        if self._gsheets is None:
            self._gsheets = GSheets(self.gsuite_secret_id)
        return self._gsheets


    def gs_project(self,title):
        result = list(self.elastic().search_on_field_for_value('Summary.keyword', title))
        if len(result) == 1:
            return result.pop()
        return None

    def gs_project_by_Id(self,key):
        result = list(self.elastic().search_on_field_for_value('Key.keyword', key))
        if len(result) == 1:
            return result.pop()
        return None


    def gs_projects(self):
        return list(self.elastic().search_on_field_for_value('Issue Type','Project'))

    def gs_projects_by_id(self):
        projects = {}
        for item in self.gs_projects():
            projects[item.get('Key')] = item
        return projects

    def gs_projects_by_title(self):
        projects = {}
        for item in self.gs_projects():
            projects[item.get('Summary')] = item
        return projects

    def gs_services(self):
        return list(self.elastic().search_on_field_for_value('Issue Type','"Service"'))

    def gs_services_by_id(self):
        services = {}
        for item in self.gs_services():
            services[item.get('Key')] = item
        return services

    def gs_services_by_title(self):
        services = {}
        for item in self.gs_services():
            services[item.get('Summary')] = item
        return services


    def set_slide_title_request(self, slide_id, title):
        title_id = '{0}_title'.format(slide_id)
        return self.gslides().element_set_text_requests(self.file_id, title_id, title)

    def set_slide_link_requests(self, slide_id, jira_key):
        link_id = '{0}_link'.format(slide_id)
        requests = self.gslides().element_set_text_requests(self.file_id, link_id, jira_key)
        requests.extend([{ 'updateTextStyle': { 'objectId': link_id,
                                                'style'   : { 'link': { 'url': self.jira_link.format(jira_key) } },
                            'fields': 'link'  }}])
        return requests

    def set_slide_link(self, slide_id, jira_key):
        return self.set_slide_link_requests(slide_id, jira_key)


    def set_table_text_request(self, slide_id, row, col, text):
        table_id = "{0}_table".format(slide_id)
        return self.gslides().element_set_table_text_requests(table_id, row, col, text)



    # main methods with business logic
    def create_slide_with_project_data(self, jira_key):
        project_data      = self.gs_project_by_Id(jira_key)
        slide_id          = 'project-{0}'.format(jira_key)
        title             = project_data.get('Summary')
        it_system         = str(project_data.get('Issue Links').get('affects'))
        risks             = str(project_data.get('Issue Links').get('fixes' ))
        gs_services       = str(project_data.get('Issue Links').get('uses'  ))
        description       = project_data.get('Description')
        pilar             = 'TBD'
        status            = project_data.get('Status')
        management_owner  = 'TBD'
        risk_owner        = 'TBD' #project_data.get('Risk Owner','TBD')
        vulns             = '...'
        budget            = 'TBD'
        business_services = 'TBD'

        self.get_slide(slide_id)
        requests = []
        requests.extend(self.set_slide_title_request(slide_id, title))
        requests.extend(self.set_slide_link (slide_id, jira_key))

        requests.extend(self.set_table_text_request (slide_id, 0, 0, it_system))
        requests.extend(self.set_table_text_request (slide_id, 0, 2, management_owner))
        requests.extend(self.set_table_text_request (slide_id, 0, 3, pilar))
        requests.extend(self.set_table_text_request (slide_id, 0, 4, risk_owner))
        requests.extend(self.set_table_text_request (slide_id, 1, 1, description))
        requests.extend(self.set_table_text_request (slide_id, 2, 1, risks))
        requests.extend(self.set_table_text_request (slide_id, 3, 1, vulns))
        requests.extend(self.set_table_text_request (slide_id, 4, 1, budget))
        requests.extend(self.set_table_text_request (slide_id, 5, 0, gs_services))
        requests.extend(self.set_table_text_request (slide_id, 5, 3, status))
        requests.extend(self.set_table_text_request (slide_id, 5, 2, business_services))
        self.gslides().execute_requests(self.file_id,requests)


    def create_slides_with_graphs(self, jira_key):
        self.create_slide_with_two_graphs('graph_{0}_gs_services_none'.format(jira_key)     ,
                                          '{0} - GS Services'.format(jira_key)              ,
                                          ('GS Services', jira_key , '3', 'uses,is child of'),
                                           None)
        self.create_slide_with_two_graphs('graph_{0}_risks_stakeholders'.format(jira_key)     ,
                                          '{0} - Risks and Stakeholders'.format(jira_key)     ,
                                          ('Risks'       , jira_key, '7', 'fixes,risks_up,creates VULN'),
                                          ('Stakeholders', jira_key, '7','affects,stakeholders_up'      ))


    def create_slides_with_projects_and_services(self, function_name, projects_key, services_key):
        #Dev.print("create_slides_with_projects_and_services: {0}  {1} {2}".format(function_name, projects_key, services_key))
        self.create_slide_with_one_graph('graphs_gs_projects',
                                         '{0} Projects'.format(function_name),
                                         (projects_key, '1', 'delivered by'))


        self.create_slide_with_one_graph('graphs_gs_services',
                                         '{0} Services'.format(function_name),
                                          (services_key, '1', 'is parent of'))

    def set_slides_positions(self,projects_ids):

        requests = []
        index = 1
        def set_position(slide_id):
            nonlocal index
            requests.extend(self.gslides().slide_move_to_pos_request(self.file_id, slide_id,index))
            index += 1


        set_position('graphs_gs_projects')
        set_position('graphs_gs_services')

        for jira_key in projects_ids:
            set_position('project-{0}'                  .format(jira_key))
            set_position('graph_{0}_gs_services_none'   .format(jira_key))
            set_position('graph_{0}_risks_stakeholders' .format(jira_key))

        set_position(self.master_slide)
        set_position(self.master_graphs_slide_id)
        self.gslides().execute_requests(self.file_id,requests)

    def export_to_pdf(self, function_name):
        target_file = '/tmp/gs_{0}_slides.pdf'.format(function_name)
        gdrive = self.gdrive()
        return gdrive.file_export_as_pdf_to(self.file_id, target_file)

    def create_slides_for_function___Cloud(self):
        projects_key = 'GSSP-116'
        services_key = 'IA-418'
        function_name = 'Cloud'
        self.create_slides_with_projects_and_services(function_name, projects_key, services_key)

        #service_ids  = self.elastic().get_data(services_key).get('_source').get('Issue Links').get('is parent of')
        projects_ids = self.elastic().get_data(projects_key).get('_source').get('Issue Links').get('delivered by')

        #projects_ids = projects_ids#[:4]

        for jira_key in projects_ids:
            self.create_slide_with_project_data(jira_key)
            self.create_slides_with_graphs(jira_key)

        self.set_slides_positions(projects_ids)




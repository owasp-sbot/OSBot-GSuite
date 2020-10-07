

from osbot_gsuite.apis.create_slides.GSBot_Helpers       import GSBot_Helper
from osbot_gsuite.apis.create_slides.GSBot_to_GDrive     import GSBot_to_GDrive
from osbot_gsuite.apis.create_slides.Slides_for_Projects import Slides_for_Projects
from osbot_utils.utils.Dev import Dev
from osbot_utils.utils import Misc


class Project_Slides:
    def __init__(self):
        self.file_id      = None
        self.file_type    = None
        self.jira_key     = None
        self.title        = None
        self._project     = None
        self._slides_ids  = None
        self.gsuite_secret_id    = 'gsuite_gsbot_user'
        self.jira_link           = 'https://jira.photobox.com/browse/{0}'
        self.slides_for_projects = Slides_for_Projects(self.gsuite_secret_id)

    def gdrive (self): return self.slides_for_projects.gdrive()
    def gslides(self): return self.slides_for_projects.gslides()

    def project(self):
        if self._project is None:
            self._project = self.slides_for_projects.gs_project_by_Id(self.jira_key)
            if self._project:
                # remove fields that we don't need to see in the main slides
                for field in ['Brands','Components','Created','Creator', 'Epic Link',
                              'Impacts','Latest_Information','Likelihood','Parent',
                              'Project', 'Reporter', 'Risk Owner','Updated',
                              'ISO27001 Standard','GDPR Article']:
                    del self._project[field]

                # fix description field
                if self._project.get('Description') is None:
                    self._project['Description'] = 'No description, please add one one using the link below'
                self._project['Description'] = Misc.remove_html_tags(self._project['Description'])

        return self._project

    def fix_slide_id(self,text):
        return text.replace(' ', '_').replace('(', '_').replace(')', '_')

    def slides_ids(self):
        if self._slides_ids is None:
            self._slides_ids = list(set(self.gslides().slides_indexed_by_id(self.file_id)))
        return self._slides_ids

    def delete_presentation(self,jira_key=None):
        if jira_key:
            self.resolve_file_id(jira_key)
        self.gdrive().file_delete(self.file_id)
        return self

    def delete_slide(self, slide_id):
        if slide_id in self.slides_ids():
            self.gslides().slide_delete(self.file_id, slide_id)
            self._slides_ids.remove(slide_id)
        return self

    def delete_all_content_slides(self):
        for slide_id in list(self.slides_ids()):
            if slide_id != 'slide_title':
                self.delete_slide(slide_id)
        return self

    def resolve_file_id(self, jira_key):
        self.jira_key = jira_key
        project = self.project()
        if project:
            summary = project.get("Summary")
            self.title = "GS Project - {0} - {1}".format(jira_key, summary)

            file = self.gdrive().find_by_name(self.title)
            if file is None:
                template_file_id = '1oApT1ujAcPuw_zMk8O5fVew9Mo4xNA28VHdLoq5DfX0'
                parent_folder    = '16yOkKyi0TfOy3w4IMW40vo-pr--Wa1Y9'
                self.file_id = self.gslides().presentation_copy(template_file_id, self.title, parent_folder)
            else:
                self.file_id = file.get('id')
        return self

    def set_jira_key(self, new_key):
        self._project = None       # force data reload
        self.jira_key = new_key
        return self
    # slides 'add helpers'

    def create_slide(self, requests, slide_id, title, x=10, y=10, width=500, height=50, size=26):
        slide_id = self.fix_slide_id(slide_id)
        self.delete_slide(slide_id)
        title_id = '{0}_title'.format(slide_id)
        requests.extend([ self.gslides().slide_create_request                      (slide_id,                             ),
                          self.gslides().element_create_shape_request              (slide_id, x,y,width, height, title_id  ),
                          self.gslides().element_insert_text_request               (title_id,title                        ),
                          self.gslides().element_set_text_style_requests__for_title(title_id, size                         )])
        return self

    def add_text(self, requests, slide_id, text, x, y, width, height,size=None, bullets= False):
        text_id = Misc.random_string_and_numbers(6, 'text_')
        requests.extend([self.gslides().element_create_shape_request              (slide_id, x, y, width, height, text_id ),
                         self.gslides().element_insert_text_request               (text_id ,text                         )])
        if size:
            requests.append({'updateTextStyle': {'objectId': text_id,
                                                 'style': {'fontSize': {'magnitude': size, 'unit': 'PT'}},
                                                 'fields': 'fontSize'}})


        if bullets:
            requests.append({"createParagraphBullets": { "objectId": text_id,
                                                         "bulletPreset": "BULLET_ARROW_DIAMOND_DISC",
                                                         "textRange": { "type": "ALL" }}})

        return self

    def add_text_with_keys_titles(self, requests, slide_id, keys, x, y, width, height, size=None):
        if not keys: return self

        issues = list(self.slides_for_projects.elastic().search_on_field_for_values("Key.keyword", keys))
        text = ''
        for issue in issues:
            text += "{0} \n".format(issue.get('Summary'))
        text = text.strip()
        return self.add_text(requests, slide_id, text, x, y, width, height, size, bullets=True)


    def add_link(self, requests, slide_id, text, link, x, y, width, height, size=None):
        text_id = Misc.random_string_and_numbers(6, 'text_')
        requests.extend([self.gslides().element_create_shape_request              (slide_id, x, y, width, height, text_id ),
                         self.gslides().element_insert_text_request               (text_id ,text                          ),
                         self.gslides().element_set_text_style_requests           (text_id, {'link': {'url': link }},'link'   )])
        if size:
            requests.append({'updateTextStyle': {'objectId': text_id,
                                                 'style': {'fontSize': {'magnitude': size, 'unit': 'PT'}},
                                                 'fields': 'fontSize'}})

        return self

    def add_image_from_expanded_graph(self, requests, slide_id, graph_name, depth, links_path):
        png_file  = GSBot_Helper().get_png_from_expanded_graph(graph_name, depth,links_path)
        image_id  = GSBot_to_GDrive(self.gsuite_secret_id).upload_png_file_to_gdrive(png_file)
        image_url = "https://lh3.google.com/u/1/d/{0}".format(image_id)
        requests.append(self.gslides().element_create_image_request(slide_id, image_url, 10, 70, 600, 300))

    def add_image_from_new_graph(self, requests, slide_id, start, direction, depth, view):
        png_file  = GSBot_Helper().get_png_from_new_graph(start, direction, depth, view)
        image_id  = GSBot_to_GDrive(self.gsuite_secret_id).upload_png_file_to_gdrive(png_file)
        image_url = "https://lh3.google.com/u/1/d/{0}".format(image_id)
        requests.append(self.gslides().element_create_image_request(slide_id, image_url, 10, 70, 600, 300))

    def add_image_from_elk_dashboard(self, requests, slide_id, jira_key,x, y, width,height):
        png_file  = GSBot_Helper().get_png_from_elk_dashboard(jira_key)
        image_id  = GSBot_to_GDrive(self.gsuite_secret_id).upload_png_file_to_gdrive(png_file)
        image_url = "https://lh3.google.com/u/1/d/{0}".format(image_id)
        requests.append(self.gslides().element_create_image_request(slide_id, image_url, x, y, width,height))
        return self

    def add_image_from_browser_risks(self, requests, slide_id, risks,x, y, width,height):
        png_file  = GSBot_Helper().get_png_from_browser_risks(risks)
        image_id  = GSBot_to_GDrive(self.gsuite_secret_id).upload_png_file_to_gdrive(png_file)
        image_url = "https://lh3.google.com/u/1/d/{0}".format(image_id)
        requests.append(self.gslides().element_create_image_request(slide_id, image_url, x, y, width,height))
        return self


    def add_new_graph(self, title, start, direction, depth, view):
        if self.project():
            slide_id  = 'slide_' + title.replace(' ', '_').replace('(', '_').replace(')', '_')
            jira_link = self.jira_link.format(start)
            requests = []
            (
                self.create_slide                 (requests, slide_id, title                         ),
                self.add_image_from_new_graph     (requests, slide_id, start, direction, depth, view ),
                self.add_link                     (requests, slide_id, start, jira_link, 630, 330, 700, 50)
            )
            self.gslides().execute_requests(self.file_id, requests)
        return self

    def add_expanded_graph(self, title, graph_name, depth, links_path):
        if self.project():
            slide_id        = 'slide_' + title.replace(' ','_').replace('(','_').replace(')','_')
            requests = []
            (
                self.create_slide                 (requests, slide_id, title                        )
                    .add_image_from_expanded_graph(requests, slide_id, graph_name, depth, links_path)
            )
            self.gslides().execute_requests(self.file_id, requests)
        return self

    def add_project_1_pager(self, jira_key,with_images=True):
        self.set_jira_key(jira_key)
        if self.project():
            issue_data      = self.project()
            slide_id        = 'slide_project_{0}'.format(jira_key)
            title           = issue_data.get('Summary')
            jira_link       = self.jira_link.format(jira_key)
            description     = Misc.remove_html_tags(issue_data.get('Description'))
            fixes           = issue_data.get('Issue Links').get('fixes')
            if not fixes:
                fixes       = issue_data.get('Issue Links').get('reduces risk of')  # for now add these if no 'fixes' exists
            text_why        = 'Why are we doing this project (i.e. what does it fix):'
            #Dev.pprint(self.project())
            r2s = GSBot_Helper().find_R2s_for_jira_issue(jira_key)
            r2s_issues = list(self.slides_for_projects.elastic().search_on_field_for_values("Key.keyword", r2s))
            risks = []
            for r2_issue in r2s_issues:
                risks.append("r{0}:2".format(r2_issue.get('Summary').split('-')[0].replace('.','_').strip()))
            risks = ','.join(risks)
            Dev.pprint(risks)
            requests = []

            (
                self.create_slide                 (requests, slide_id, title         , size =20)
                    .add_link                     (requests, slide_id, self.jira_key, jira_link,  390, 375, 700,  60 ,6)
                    .add_text                     (requests, slide_id, description   , 10,  70, 400,100, 9)
                    .add_text                     (requests, slide_id, text_why      , 10, 210, 400,100, 14)
                    .add_text_with_keys_titles    (requests, slide_id, fixes         , 10, 240, 400, 100, 9)
            )
            self.gslides().execute_requests(self.file_id, requests)

            if with_images:
                requests = []
                self.add_image_from_elk_dashboard (requests, slide_id, jira_key      , 450,  -40, 260, 360)
                self.gslides().execute_requests(self.file_id, requests)

                requests = []
                self.add_image_from_browser_risks (requests, slide_id, risks         , 450,  230 , 260, 210)
                self.gslides().execute_requests(self.file_id, requests)
            
        return self

        
    # Creating Slide's content

    def set_content_title_slide(self, slide_type=None):
        if self.project():
            if slide_type is None: slide_type = 'GS Project'
            title    = self.project().get('Summary')
            subtitle = "{0} : {1}".format(slide_type,self.project().get('Key'))
            self.gslides().element_set_text(self.file_id, 'slide_title___title'    , title)
            self.gslides().element_set_text(self.file_id, 'slide_title___subtitle' , subtitle)
        return self

    def add_slide_with_title(self):
        data       = self.project()
        key        = data.get('Key')
        summary    = data.get('Summary')
        issue_type = data.get('Issue Type')
        jira_link = self.jira_link.format(key)
        requests   = []
        slide_id = self.fix_slide_id('slide_{0}'.format(summary))
        (
            self.create_slide(requests, slide_id, summary, 100,100,500,250,50)
                .add_text    (requests, slide_id, issue_type, 100,250,500,250)
                .add_link    (requests, slide_id, key, jira_link, 630, 330, 700, 50)
        )

        self.gslides().execute_requests(self.file_id, requests)
        return self

    def add_slide_project_details(self):
        if self.project():
            slide_id        = 'slide_project_details'
            title           = 'Project Details'.format(self.jira_key)
            description     = self.project().get('Description')
            jira_link       = self.jira_link.format(self.jira_key)
            requests        = []
            (
                self.create_slide(requests, slide_id, title                                         )
                    .add_text    (requests, slide_id, description,                10, 100, 650, 150 )
                    .add_link    (requests, slide_id, self.jira_key, jira_link,  630, 330, 700,  50 )
            )
            self.gslides().execute_requests(self.file_id, requests)
        return self

    def add_slide_with_table_with_key_details(self, name, keys):
        max_text_size = 450
        if keys is None: keys = []
        services = list(self.slides_for_projects.elastic().search_on_field_for_values("Key.keyword", keys))
        table_data = [['Jira Id', 'Title', 'Description' ]]

        for service in services:
            jira_key    = service.get('Key')
            title       = service.get('Summary')
            description = service.get('Description')
            if description is None: description = 'No Description, please add one in Jira'
            description = Misc.remove_html_tags(description).replace('\n',' ')
            description = (description[:max_text_size] +  ' ...') if len(description) > max_text_size else description
            table_data.append([jira_key,title,description])
        slide_id = 'slide_{0}'.format(name.lower()).replace(' ','_').replace('(','_').replace(')','_')
        title    = '{0}'.format(name)
        table_id = self.gslides().add_slide_with_table_from_array(self.file_id, slide_id, title, table_data,[50,100,545])

        requests = []
        for index, row in enumerate(table_data):
            jira_id = row.pop(0)
            link = self.jira_link.format(jira_id)
            requests.append(self.gslides().element_set_table_text_style_request(table_id, index +1 ,0,{'link': {'url': link }},'link'))

        self.gslides().execute_requests(self.file_id,requests)

    def add_slide_with_issues_linked(self, link_type, name, max_rows  = 6):
        keys = self.project().get('Issue Links').get(link_type)
        if keys:
            size      = len(keys)
            page      = 0
            max_pages = round( (size+1) /max_rows)
            for i in range(0, size, max_rows):
                page  +=1
                title = "{0} ({1} of {2})".format(name, page, max_pages)
                values = keys[i:i + max_rows]
                self.add_slide_with_table_with_key_details(title,values)
        return self

    def add_slide_services_used(self): return self.add_slide_with_issues_linked('uses'           , "Services Used")
    def add_slide_risks_reduced(self): return self.add_slide_with_issues_linked('reduces risk of', "Risks Reduced")
    def add_slide_delivers     (self): return self.add_slide_with_issues_linked('delivers'       , "Delivers")
    def add_slide_affects      (self): return self.add_slide_with_issues_linked('affects'        , "Affects"      )

    def add_slide_with_graph_risks_to_R1 (self): return self.add_expanded_graph  ('Graph - Risks (path to R1)', self.jira_key       , 5, 'risks_up'                        )
    def add_slide_with_graph_stakeholders(self): return self.add_expanded_graph  ('Graph - Stakeholders'      , self.jira_key       , 5, 'risks_up,affects,stakeholders_up')
    def add_slide_with_graph_all_1       (self): return self.add_new_graph       ('Graph (all nodes depth 1)' , self.jira_key, 'all', 1, 'colors'                          )

    def add_slide_with_project_1_pager   (self, project_id,with_images=True):
        try:
            return self.add_project_1_pager(project_id,with_images)
        except Exception as error:
            Dev.pprint("[add_slide_with_project_1_pager][error] {0}".format(error))
            return self


    def add_slides_with_project_1_pager  (self, project_ids):
        for project_id in project_ids:
            self.add_slide_with_project_1_pager(project_id)
        return self

    def add_metadata_slide(self):
        if self.project():
            del self._project['Description']
            slide_id = 'slide_metadata'
            title    = 'Project {0} Metadata'.format(self.jira_key)
            #self.gslides().slide_delete(self.file_id, slide_id)                         # this one needs to be done outside since it will fail on first creation
            self.gslides().add_slide_with_table_from_object(self.file_id, slide_id, title, self.project())
        return self


    def create_slides_text_content(self, jira_key):
        (
            self.resolve_file_id                 (jira_key)
                .delete_all_content_slides       ()
                .set_content_title_slide         ()
                #.add_slide_project_details       ()
                .add_slide_with_project_1_pager  (jira_key)
                .add_slide_services_used         ()
                .add_slide_risks_reduced         ()
                .add_slide_delivers()
                .add_slide_affects               ()
        )
        return self.gdrive().file_weblink(self.file_id)

    def create_slides_graphs(self):
        (
            self.add_slide_with_graph_risks_to_R1()
                .add_slide_with_graph_stakeholders()
                .add_slide_with_graph_all_1()
        )
        return self

    def create_slides_appendix(self):
        (
            self.add_metadata_slide()
        )
        return self



    # Function Slides generation (move to separate file

    def add_slide_function_details(self):
        if self.project():
            slide_id        = 'slide_function_details'
            title           = 'Function Details'.format(self.jira_key)
            description     = self.project().get('Description')
            jira_link       = self.jira_link.format(self.jira_key)
            requests        = []
            (
                self.create_slide(requests, slide_id, title                                         )
                    .add_text    (requests, slide_id, description,                10, 100, 650, 150 )
                    .add_link    (requests, slide_id, self.jira_key, jira_link,  630, 330, 700,  50 )
            )
            self.gslides().execute_requests(self.file_id, requests)

        return self

    def create_slides_for_function(self, key_function):
        (
            self.resolve_file_id             (key_function)
                .delete_all_content_slides   ()
                .set_content_title_slide     ("GS Function")
                .add_slide_function_details  ()
        )

        keys = self.project().get('Issue Links').get('is parent of')

        for key in keys:
            self.set_jira_key(key)
            title      = self.project().get('Summary')
            issue_type = self.project().get('Issue Type')
            self.add_slide_with_title()
            if issue_type == 'Programme':
                self.add_slide_with_issues_linked('delivered by', title) #"Projects")
            if issue_type == 'Business entity':
                self.add_slide_with_issues_linked('is parent of', title) #"Services")


        #         .set_jira_key                (key_projects)
        #         .add_slide_with_issues_linked('delivered by', "Projects")
        #         .set_jira_key                (key_services)
        #         .add_slide_with_issues_linked('is parent of', "Services")
        #
        #         #.add_new_graph          ('key_projects' , key_projects, 'all', 1, 'colors')
        #         #.add_new_graph          ('key_services' , key_services , 'all', 1, 'colors')
        # )
        return self.gdrive().file_weblink(self.file_id)


    def create_project_slides_for_functions(self, key_function,team_id, channel):
        (
            self.resolve_file_id             (key_function)
                .delete_all_content_slides   ()
                .set_content_title_slide     ("PROJECTS")
        )
        delivered_by = self.project().get('Issue Links').get('delivered by')
        delivered_by.remove('GSSP-327')        # for now manually remove this project (GSP BAU)

        #weblink = self.gdrive().file_weblink(self.file_id)
        #slack_message(':point_rigth: batch creating slides for {0}'.format(self.project))

        issues = list(self.slides_for_projects.elastic().search_on_field_for_values("Key.keyword", delivered_by))
        for issue in issues:
            try:
                if issue.get('Key') == 'GSSP-118': continue #skip fix since it has been done
                #if issue.get('Key') == 'GSSP-120': continue # detect
                #if issue.get('Key') == 'GSSP-121': continue # risk
                if issue.get('Key') == 'GSSP-113': continue # gs internal
                if issue.get('Key') == 'GSSP-115': continue # infosec
                self.set_jira_key(issue.get('Key'))
                if self.project():
                    self.add_slide_with_title()
                    delivered_by = self.project().get('Issue Links').get('delivered by')
                    for project in delivered_by:
                        self.add_slide_with_project_1_pager(project)
            except Exception as error:
                Dev.pprint('[create_project_slides_for_functions][error] {0}'.format(error))

        return self.gdrive().file_weblink(self.file_id)
from time import time

from osbot_aws.helpers.Lambda_Helpers import slack_message
from osbot_gsuite import version_osbot_gsuite
from osbot_gsuite.apis.create_slides.Project_Slides              import Project_Slides
from osbot_gsuite.apis.create_slides.Slides_for_Projects         import Slides_for_Projects

class Slides_Commands:

    @staticmethod
    def _gs_functions_ids():
        slides_for_projects = Slides_for_Projects()
        key = 'IA-402'
        issue = list(slides_for_projects.elastic().search_on_field_for_value('Key.keyword', key)).pop(0)
        return  issue.get('Issue Links').get('is parent of')

    @staticmethod
    def gs_functions(team_id, channel, params):
        slides_for_projects = Slides_for_Projects()

        functions = list(slides_for_projects.elastic().search_on_field_for_values('Key.keyword', Slides_Commands._gs_functions_ids()))
        attachment_text = ''
        for function in functions:
            key     = function.get('Key')
            summary = function.get('Summary')
            link    = 'https://jira.photobox.com/browse/{0}'.format(key)
            attachment_text += ' <{0}|{1}>  - {2} \n'.format(link, summary, key)
        text = ':point_right: Here is the current list of GS Functions (use `slides create {{jira id}}` to create the slides:) '
        attachments = [{'text': attachment_text}]
        return text, attachments

    @staticmethod
    def gs_projects(team_id, channel, params):
        slides_for_projects = Slides_for_Projects()
        #if len(params) ==0 :

        projects = slides_for_projects.gs_projects_by_title()
        text        = ':point_right: Here is the current list of `{0}` GS Projects (use `slides create {{jira id}}` to create the slides:) '.format(len(projects))
        attachment_text=''

        for index, title in enumerate(sorted(projects.keys())):
            project = projects[title]
            key   = project.get('Key')
            attachment_text += '{0}. {1}  - {2} \n'.format(index + 1,title, key)  # can't use the link here since it will get top big and slack will not show all results
        attachments = [{'text': attachment_text }]
        return text,attachments

    @staticmethod
    def create(team_id, channel, params):
        try:
            jira_key = params.pop(0)
            options  = ''
            if len(params) > 0: options  = params.pop(0)
            # jira_link = 'https://jira.photobox.com/browse/{0}'.format(jira_key)
            # slack_message(":zero: Creating slides for project: `{0}` (which you can edit in jira :point_right: <{1}|here>)".format(jira_key,jira_link), [],channel, team_id)jira_key = params.pop(0)

            jira_link = 'https://jira.photobox.com/browse/{0}'.format(jira_key)
            slack_message(":one: Creating slides for: `{0}` (which you can edit in jira :point_right: <{1}|here>)".format(jira_key,jira_link), [],channel, team_id)
            project_slides = Project_Slides()
            start = time()

            if jira_key in Slides_Commands._gs_functions_ids(): # is an GS Function
                slack_message(":two: Creating slides for Function `{0}`".format(jira_key), [],channel, team_id)
                weblink = project_slides.create_slides_for_function(jira_key)
            else:
                weblink = project_slides.create_slides_text_content(jira_key)
                if options == 'no_graphs':
                    slack_message(":one: ...skipping graph creation...", [],channel, team_id)
                else:
                    slack_message(":two: Currently adding the graphs for project `{0}`, but if you want, click <{1}|here to open the Slides>".format(jira_key,weblink), [],channel, team_id)
                    project_slides.create_slides_graphs()           \
                                  .create_slides_appendix()
            duration = time()-start
            return ":three: Slide creation complete. You can see it at <{2}|{0} Project slides>  \n :point_right: _creation duration: `{1:.0f}` secs_\n :point_right: _create pdf using: `gdocs pdf {3}`_".format(jira_key, duration,weblink, project_slides.file_id),[]
        except Exception as error:
            slack_message("Error presentation for project: `{0}`: {1}".format(jira_key,error), [], channel, team_id)
        return None,None

    @staticmethod
    def gs_services(team_id, channel, params):
        slides_for_projects = Slides_for_Projects()
        services = slides_for_projects.gs_services_by_title()
        text = ':point_right: Here is the current list of `{0}` GS Services: '.format(len(services))
        attachment_text = ''

        for index, title in enumerate(sorted(services.keys())):
            service = services[title]
            key  = service.get('Key')
            link  = 'https://jira.photobox.com/browse/{0}'.format(key)
            attachment_text += ' {0}.  <{1}|{2}>  - {3} \n'.format(index + 1 , link, title, key)
        attachments = [{'text': attachment_text}]
        return text, attachments


    @staticmethod
    def create_projects(team_id, channel, params):
        key = 'GSSP-112'            # FY20 projects
        Project_Slides().create_project_slides_for_functions(key,team_id,channel)

    @staticmethod
    def version(team_id, channel, params):
        return version_osbot_gsuite
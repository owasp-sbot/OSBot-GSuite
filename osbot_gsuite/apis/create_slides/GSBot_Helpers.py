import base64
import json

from osbot_aws.apis.Lambda import Lambda
from osbot_elastic.Elastic_Search import Elastic_Search
from osbot_utils.utils.Files import Files


class GSBot_Helper:

    def elastic__setup_elk(self):
        index           = 'save_to_elk'
        secrets_elastic = 'elastic-logs-server-1'
        return Elastic_Search()._setup_Elastic_on_cloud_via_AWS_Secret(index, secrets_elastic)

    def create_graph(self, start, direction, depth,view=None):
        lambda_graph = Lambda('pbx_gs_python_utils.lambdas.gs.elastic_jira')

        payload = { "params": ['links', start, direction, depth,view] }
        result = lambda_graph.invoke(payload)
        data = json.loads(result.get('text'))
        return data

    def expand_graph(self, graph_name, depth,links_path):
        lambda_graph = Lambda('lambdas.gsbot.gsbot_graph')

        payload = { 'data': {}, "params": ['expand', graph_name, depth, links_path]}
        result = lambda_graph.invoke(payload)
        return json.loads(result)

    def get_png_from_expanded_graph(self, graph_name, depth,links_path):
        target_file = '/tmp/puml_{0}_{1}_{2}.png'.format(graph_name, depth,links_path)
        #if Files.not_exists(target_file):
        graph_metadata = self.expand_graph(graph_name, depth,links_path)
        self.puml_to_png(graph_metadata.get('puml'), target_file)
        return target_file

    def find_R2s_for_jira_issue(self, jira_key):
        r2s = []
        graph_metadata = self.expand_graph(jira_key, 10, 'risks_up')
        for edge in graph_metadata.get('edges'):
            if edge[1] == 'creates R2':
                r2s.append(edge[2])
        return list(set(r2s))

    def get_png_from_new_graph(self, start, direction, depth, view=None):
        target_file = '/tmp/puml_{0}_{1}_{2}.png'.format(start,direction,depth)
        #if Files.not_exists(target_file):
        graph_metadata = self.create_graph(start,direction,depth,view)
        self.puml_to_png(graph_metadata.get('puml'), target_file)
        return target_file

    def get_png_from_saved_graph(self, graph_name, target_file=None):
        if target_file is None:
            target_file  = '/tmp/puml_{0}.png'.format(graph_name)
        else:
            Files.delete(target_file)
        if Files.not_exists(target_file):
            lucene_query = 'doc_data.name:"{0}"'           .format(graph_name)
            result       = self.elastic__setup_elk().search_using_lucene_index_by_id(lucene_query, 1, "date:desc").values()
            puml         =  list(result)[0].get('doc_data').get('extra_data').get('puml')
            self.puml_to_png(puml, target_file)

        return target_file

    def get_png_from_elk_dashboard(self, jira_key):
        png_file = '/tmp/puml_elk_dashboard_{0}.png'.format(jira_key)
        lambda_browser = Lambda('browser.lambda_browser')

        payload = {"params": ['elk', 'dashboard_project', jira_key]}
        png_data = lambda_browser.invoke(payload)
        with open(png_file, "wb") as fh:
            fh.write(base64.decodebytes(png_data.encode()))
        return png_file

    def get_png_from_browser_risks(self, risks):
        #png_file = '/tmp/puml_browser_risks_{0}.png'.format(jira_key)
        png_file = Files.temp_file(".png")
        lambda_browser = Lambda('lambdas.browser.lambda_browser')

        payload = {"params": ['risks', risks]}
        png_data = lambda_browser.invoke(payload)
        with open(png_file, "wb") as fh:
            fh.write(base64.decodebytes(png_data.encode()))
        return png_file



    def puml_to_png(self, puml, target_file):
        puml_to_png = Lambda('utils.puml_to_png')
        png_data = puml_to_png.invoke({"puml": puml})

        with open(target_file, "wb") as fh:
            fh.write(base64.decodebytes(png_data['png_base64'].encode()))
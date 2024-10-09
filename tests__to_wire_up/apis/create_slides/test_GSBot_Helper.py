import sys ; sys.path.append('..')

from unittest import TestCase
from pbx_gs_python_utils.utils.Files import Files
from osbot_gsuite.apis.create_slides.GSBot_Helpers import GSBot_Helper


class test_GSBot_Helpers(TestCase):

    def setUp(self):
        self.gsbot_helper = GSBot_Helper()

    def test_expand_graph(self):
        result = self.gsbot_helper.expand_graph('GSSP-128', 7, 'fixes,risks_up,creates VULN')
        #Dev.pprint(result)

    def test_get_png_from_saved_graph(self):
        # graph_name = 'graph_W64'
        target_file = '/tmp/puml_graph.png'
        #graph_name  = 'graph_29E'  # one node
        graph_name  = 'graph_9ML' #'graph_09Q'
        png_file = self.gsbot_helper.get_png_from_saved_graph(graph_name, target_file)
        assert Files.exists(png_file)

    def test_get_png_from_new_graph(self):
        result = self.gsbot_helper.get_png_from_new_graph('IA-386','down','2')
        assert Files.exists(result)

    def test_get_png_from_expanded_graph(self):
        result = self.gsbot_helper.get_png_from_expanded_graph('GSSP-128', 7, 'fixes,risks_up,creates VULN')
        assert Files.exists(result)

    # def test___run_lambda(self):
    #     lambda_graph = Lambda('pbx_gs_python_utils.lambdas.gs.elastic_jira')
    #
    #     payload = {
    #         "params": ['links','IA-386','down','15']
    #     }
    #     result = lambda_graph.invoke(payload)
    #     Dev.pprint(result)
    #     return
    #     data = json.loads(result.get('text'))
    #     print()
    #     print('text' , len(result.get('text')))
    #     print('puml' , len(data  .get('puml')))
    #     print('nodes', len(data  .get('nodes')))
    #     print('edges', len(data  .get('edges')))
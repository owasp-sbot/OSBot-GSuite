from osbot_aws.apis.Lambda import load_dependencies
from pbx_gs_python_utils.utils.Lambdas_Helpers import log_to_elk


def run(event, context):
    try:
        load_dependencies(["gmail", "elastic-slack", 'requests'])                                    # load dependency (download and unzip if first run)
        from osbot_gsuite.apis.handlers.Lambda_Slides import Lambda_Slides
        return Lambda_Slides().handle_lambda_event(event)                                   # invoke lambda handler from Lambda_Slides class

        #return "200 OK"

    except Exception as error:
        message = "[lambda_slides] Error: {0}".format(error)
        log_to_elk(message, level='error')
        return message
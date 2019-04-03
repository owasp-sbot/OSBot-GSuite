
from pbx_gs_python_utils.utils.Lambdas_Helpers import log_to_elk
from pbx_gs_python_utils.utils.aws.Lambdas import load_dependency


def run(event, context):
    try:
        load_dependency("gmail")
        load_dependency("elastic-slack")                              # load dependency (download and unzip if first run)
        load_dependency('requests')

        from gsbot_gsuite.apis.handlers.Lambda_GDocs import Lambda_GDocs
        return Lambda_GDocs().handle_lambda_event(event)                      # invoke lambda handler from Lambda_Slides class
        return "200 OK"

    except Exception as error:
        message = "[lambda_gdocs] Error: {0}".format(error)
        log_to_elk(message, level='error')
        return message
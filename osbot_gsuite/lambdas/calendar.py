from osbot_aws.apis.Lambda import load_dependency
from pbx_gs_python_utils.utils.Lambdas_Helpers import log_to_elk


def run(event, context):
    try:
        load_dependency("gmail")
        #load_dependency("elastic-slack")                                      # load dependency (download and unzip if first run)
        from osbot_gsuite.apis.handlers.Lambda_Calendar import Lambda_Calendar
        return Lambda_Calendar().handle_lambda_event(event)                    # invoke lambda handler from Lambda_Slides class

    except Exception as error:
        message = "[lambda_gcalendar] Error: {0}".format(error)
        log_to_elk(message, level='error')
        return message
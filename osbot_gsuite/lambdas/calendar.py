from osbot_aws.helpers.Lambda_Helpers import log_to_elk
from osbot_aws.Dependencies import load_dependency


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
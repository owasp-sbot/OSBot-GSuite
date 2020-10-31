from osbot_aws.Dependencies import load_dependency
from osbot_aws.helpers.Lambda_Helpers import log_to_elk


def run(event, context):
    try:
        load_dependency("gmail")
        load_dependency("elastic")
        load_dependency("slack")
        load_dependency('requests')

        from osbot_gsuite.apis.handlers.Lambda_GDocs import Lambda_GDocs
        return Lambda_GDocs().handle_lambda_event(event)                      # invoke lambda handler from Lambda_Slides class
        return "200 OK"

    except Exception as error:
        message = "[lambda_gdocs] Error: {0}".format(error)
        log_to_elk(message, level='error')
        return message
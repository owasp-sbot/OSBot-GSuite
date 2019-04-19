from pbx_gs_python_utils.utils.Lambdas_Helpers import log_to_elk

from osbot_gsuite.apis.handlers.Lambda_Sheets import Lambda_Sheets


def run(event, context):
    try:
        from osbot_aws.apis.Lambda import load_dependency
        load_dependency("gmail")
        load_dependency("elastic-slack")                                # load dependency (download and unzip if first run)

        Lambda_Sheets().handle_lambda_event(event)                      # invoke lambda handler from Lambda_Sheets class
        return "200 OK"

    except Exception as error:
        message = "[lambda_sheets] Error: {0}".format(error)
        log_to_elk(message, level='error')
        return message
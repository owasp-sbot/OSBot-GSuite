
from utils.Lambdas_Helpers import log_to_elk
from utils.aws.Lambdas import load_dependency


def run(event, context):
    try:
        load_dependency("gmail")
        #load_dependency("elastic-slack")                                      # load dependency (download and unzip if first run)

        from gs_budget.create_slides.Lambda_Calendar import Lambda_Calendar    # import Lambda_Calendar class
        return Lambda_Calendar().handle_lambda_event(event)                    # invoke lambda handler from Lambda_Slides class
        return "200 OK"

    except Exception as error:
        message = "[lambda_gcalendar] Error: {0}".format(error)
        log_to_elk(message, level='error')
        return message
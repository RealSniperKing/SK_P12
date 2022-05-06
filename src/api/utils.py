from rest_framework.views import exception_handler
from rest_framework.exceptions import NotFound


def custom_exception_handler(exc, context):
    """
    Custom message '404 not found'
    REST_FRAMEWORK settings : 'EXCEPTION_HANDLER': 'api.utils.custom_exception_handler'
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None and response.status_code == 404:
        response.data = {
            "message": "Instance not found.",
            "success": False
        }
    return response
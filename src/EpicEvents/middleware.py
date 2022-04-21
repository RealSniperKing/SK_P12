import logging

logger = logging.getLogger(__name__)


class PageNotFoundMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            logger.warning("------------ Page not found at {}".format(request.path) + "------------")
            logger.debug("status_code = {}".format(response.status_code))
            logger.debug("path_info = {}".format(request.path_info))
            logger.debug("scheme = {}".format(request.scheme))
            logger.debug("encoding = {}".format(request.encoding))
            logger.debug("content_type = {}".format(request.content_type))
            logger.debug("META = {}".format(request.META))
            logger.debug("method = {}".format(request.method))
            logger.debug("headers = {}".format(request.headers))
            logger.debug("user = {}".format(request.user))
            logger.debug("get_host = {}".format(request.get_host))
            logger.debug("body = {}".format(request.body))
            print("MMMMMMMM")
        return response


class PageFatalErrorMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        status_code = response.status_code
        status_codes_filter = ["5"]
        print("str(status_code)[0] = ", str(status_code)[0])
        if str(status_code)[0] in status_codes_filter:
            logger.warning("------------ Fatal error {}".format(request.path) + "------------")
            logger.debug("status_code = {}".format(response.status_code))
            logger.debug("path_info = {}".format(request.path_info))
            logger.debug("scheme = {}".format(request.scheme))
            logger.debug("encoding = {}".format(request.encoding))
            logger.debug("content_type = {}".format(request.content_type))
            logger.debug("META = {}".format(request.META))
            logger.debug("method = {}".format(request.method))
            logger.debug("headers = {}".format(request.headers))
            logger.debug("user = {}".format(request.user))
            logger.debug("get_host = {}".format(request.get_host))
            logger.debug("body = {}".format(request.body))
            print("MMMMMMMM")
        return response
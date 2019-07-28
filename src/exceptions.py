from requests import codes

class APIException(Exception):
    """ Base exception for all exceptions within this package. """

    def __init__(self, response, description):
        super().__init__(f"Error with request {response}: {description}")

class ServerException(APIException):
    """ Indicate issues on server side. """
    def __init__(self, response):
        super().__init__(response, "Issues on server side.")

class BadRequest(APIException):
    """ Indicate invalid parameters for the request. """
    def __init__(self, response):
        super().__init__(response, "Invalid parameters for request.")

class Unauthorized(APIException):
    """ Indicate missing or incorrect authentication for the request. """
    def __init__(self, response):
        super().__init__(response, "Missing or incorrect authentication.")

class Forbidden(APIException):
    """ Indicate that this request is not permitted. """
    def __init__(self, response):
        super().__init__(response, "Access not permitted.")

class NotFound(APIException):
    """ Indicate that the requested URL cannot be found. """
    def __init__(self, response):
        super().__init__(response, "URL cannot be found.")

class Redirect(APIException):
    """ Indicate that the request resulted in a redirect. """
    def __init__(self, response):
        super().__init__(response, "Redirect encountered.")

class LegalReasons(APIException):
    """ Indicate that the requested URL is not available for legal reasons. """
    def __init__(self, response):
        super().__init__(response, "Not available for legal reasons.")

STATUS_CODE_SUCCESS = (codes["ok"], codes["created"])

STATUS_CODE_EXCEPTIONS = {
    codes["bad_gateway"]: ServerException,
    codes["bad_request"]: BadRequest,
    codes["found"]: Redirect,
    codes["forbidden"]: Forbidden,
    codes["gateway_timeout"]: ServerException,
    codes["internal_server_error"]: ServerException,
    codes["not_found"]: NotFound,
    codes["service_unavailable"]: ServerException,
    codes["unauthorized"]: Unauthorized,
    codes["unavailable_for_legal_reasons"]: LegalReasons,
    # Cloudflare status (not named in requests)
    520: ServerException,
    522: ServerException,
}
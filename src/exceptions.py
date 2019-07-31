from requests import codes

class APIException(Exception):
    """ Base exception for all exceptions related to status codes within this package. """
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

class ParameterException(Exception):
    """ Base exception for all exceptions related to incorrect parameters within this package. """
    def __init__(self, parameter, description):
        super().__init__(f"Error: Parameter \'{parameter}\' {description}")

class IncorrectType(ParameterException):
    """ Indicate that the parameter must be of param_type type. """
    def __init__(self, parameter, param_type):
        if isinstance(param_type, tuple):
            param_type = ", ".join([typ.__name__ for typ in param_type[:-1]]) + f" or {param_type[-1].__name__}"
        super().__init__(parameter, description=f"must be of type {param_type}.")

class NonPositive(ParameterException):
    """ Indicate that the parameter must be a positive integer. """
    def __init__(self, parameter):
        super().__init__(parameter, description=f"must be a positive integer.")

class IllegalSlug(ParameterException):
    """ Indicate that the parameter does not follow the rules for a slug. """
    def __init__(self, parameter):
        super().__init__(parameter, description=f"must be a nonempty string, consisting only of ascii character, with no multiple words.")

class IllegalTerm(ParameterException):
    """ Indicate that the parameter does not follow the rules for a term. """
    def __init__(self, parameter):
        super().__init__(parameter, description=f"must be a nonempty string.")

class APIKeyNotSet(ParameterException):
    """ Indicate that the parameter key has not been set properly. """
    def __init__(self, parameter):
        super().__init__(parameter, description=f"must be set before making a request.")

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
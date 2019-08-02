
import requests
from functools import wraps, singledispatch, update_wrapper
from typing import Union, List, Any, Type, Tuple, Optional

from TheNounProjectAPI.keys import Keys
from TheNounProjectAPI.exceptions import IncorrectType, NonPositive, IllegalSlug, IllegalTerm

class Core(Keys):
    """
    Core is a class providing helper functions useful for accessing the TheNounProject API.
    """

    def __init__(self, key:str = None, secret:str = None, testing:bool = False, timeout:Union[float, Tuple[float, float], None] = 5.0):
        """
        Construct a new object for making API requests.

        :param key: The API key from the TheNounProject API. (defaults to None)
        :type key: str
        :param secret: The secret key from the TheNounProject API. (defaults to None)
        :type secret: str
        :param testing: Whether the methods should return a PreparedRequest, 
                        instead of data from the API. Should not be used except for testing this wrapper. (defaults to False)
        :type testing: bool
        :param timeout: Float timeout in seconds, 2-tuples for seperate connect and read timeouts, and None for no timeout. (defaults to 5.0)
        :type timeout: Union[float, Tuple[float, float], None]
        """
        self.api_key = key
        self.secret_key = secret
        self._testing = testing
        self._timeout = timeout
        
        self._method: str
        self._base_url = "http://api.thenounproject.com"
        self._session = requests.Session()

    def _send(self, url: requests.PreparedRequest) -> requests.Response:
        """
        :param url: The PreparedRequest with the method, URL and parameters for the request.
        :type url: requests.PreparedRequest

        :returns: Returns a requests.Response object generated by performing the URL request with our session.
        :rtype: requests.Response
        """
        return self._session.send(url, timeout=self._timeout)

    def _prepare_url(self, url: str, **params: dict) -> requests.PreparedRequest:
        """
        Returns a requests.PreparedRequest object for a request self._method as method, 
        for the given URL, with the given parameters/json, with authentication.

        :param url: The URL of the requested endpoint.
        :type url: str
        :param params: The parameters to be added onto the string.
        :type params: dict

        :returns: A requests.PreparedRequest object.
        :rtype: requests.PreparedRequest 
        """
        if self._session.auth is None:
            self._session.auth = self._get_oauth()
        req = requests.Request(self._method, url, **{"params" if self._method == "GET" else "json": params})
        return self._session.prepare_request(req)

    def _type_assert(self, param: Any, param_name: str, types: Union[Type[Any], Tuple[Type[Any], ...]]) -> None:
        """
        Asserts that param is an instance of any type in types.

        :param param: Parameter to check type of.
        :type param: Any
        :param param_name: Name of this parameter, for use in error message.
        :type param_name: str
        :param types: Types to check param against. Either a single type or a tuple of types.
        :type types: Union[Type[Any], Tuple[Type[Any], ...]]

        :raise IncorrectType: Raises exception if param is not an instance of any type in types.
        """
        if not isinstance(param, types):
            raise IncorrectType(param_name, types)

    def _lop_assert(self, limit: Any, offset: Any, page: Any) -> None:
        """
        Asserts that limit, offset and page parameters are all integers.

        :param limit: Limit parameter to be used as a parameter in the URL request.
        :type limit: Any
        :param offset: Offset parameter to be used as a parameter in the URL request.
        :type offset: Any
        :param page: Page parameter to be used as a parameter in the URL request.
        :type page: Any

        :raise IncorrectType: Raises exception when limit, offset or page are not of NoneType or integer type.
        """
        NoneType = type(None)

        self._type_assert(limit, "limit", (NoneType, int))
        self._type_assert(offset, "offset", (NoneType, int))
        self._type_assert(page, "page", (NoneType, int))

    def _id_assert(self, _id: int, param_name: str) -> None:
        """
        Asserts that the _id parameter is positive.

        :param _id: Id of which we want to make sure it is positive.
        :type _id: int
        :param param_name: Name of this parameter, for use in error message.
        :type param_name: str

        :raise NonPositive: Raises exception when _id is not positive.
        """
        if _id <= 0: 
            raise NonPositive(param_name)

    def _slug_assert(self, slug: str, param_name: str) -> None:
        """
        Asserts that slug is nonempty, ascii, and does not contain spaces.

        :param slug: String slug parameter to be used as a parameter in the URL request.
        :type slug: str
        :param param_name: Name of this parameter, for use in error message.
        :type param_name: str

        :raise IllegalSlug: Raises exception when slug is empty, contains non-ascii characters, or contains spaces.
        """
        if slug.find(" ") == -1 and slug.isascii() and len(slug) > 0:
            return
        raise IllegalSlug(param_name)

    def _term_assert(self, term: str, param_name: str) -> None:
        """
        Asserts that term is nonempty.

        :param term: String term parameter to be used as a parameter in the URL request.
        :type term: str
        :param param_name: Name of this parameter, for use in error message.
        :type param_name: str

        :raise IllegalTerm: Raises exception when term has a length of 0.
        """
        if not len(term) > 0:
            raise IllegalTerm(param_name)

    def _close_session(self):
        """
        Closes the requests.Session used for making requests.
        """
        self._session.close()
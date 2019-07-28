
import requests, json
from requests import Request, Session
from requests_oauthlib import OAuth1
from functools import wraps, singledispatch, update_wrapper
from typing import Union

import exceptions

def methoddispatch(f):
    # Modified version of singledispatch to work with methods
    dispatcher = singledispatch(f)
    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)
    wrapper.register = dispatcher.register
    update_wrapper(wrapper, f)
    return wrapper

def get_endpoint(f):

    @wraps(f)
    def wrapper(self, *args, **kwargs):
        prepared_request = f(self, *args, **kwargs)
        if self.testing:
            return prepared_request

        response = self._get(prepared_request)

        api_response = APIResponse(response)
        return api_response
    
    return wrapper

class APIResponse:

    def __init__(self, response: requests.Response):
        self.response = response
        self.status_code = response.status_code
        try:
            self.json = response.json()
        except json.decoder.JSONDecodeError:
            self.json = None
        
        if self.status_code in exceptions.STATUS_CODE_EXCEPTIONS:
            raise exceptions.STATUS_CODE_EXCEPTIONS[self.status_code](self)
    
    def __str__(self):
        return f"<APIResponse [{self.status_code}] on url {self.response.url}>"
    
    def __repr__(self):
        return f"<APIResponse [{self.status_code}] on url {self.response.url}>"
    
    def __getitem__(self, item):
        if self.json is None:
            raise Exception("Response did not contain JSON, likely due to a request error. It's recommended to check the status_code before accessing this field.")
            
        return self.json[item]

class TheNounProject:
    """
    TheNounProject is a class allowing convenient access to the TheNounProject API.
    """

    def __init__(self, key:str = None, secret:str = None, testing:bool = False, timeout:Union[int, tuple, None] = 5):
        """
        Construct a new 'TheNounProject' object.

        :param key: The API key from the TheNounProject API. (defaults to None)
        :type key: str
        :param secret: The secret key from the TheNounProject API. (defaults to None)
        :type secret: str
        :param testing: Whether the 'get_...' methods should return a PreparedRequest, 
                        instead of data from the API. (defaults to False)
        :type testing: bool
        :param timeout: Integer timeout in seconds, 2-tuples for seperate connect and read timeouts, and None for no timeout. (defaults to 5)
        :type timeout: Union[int, tuple, None]
        """
        self.api_key = key
        self.secret_key = secret
        self.testing = testing
        self.timeout = timeout

        self._base_url = "http://api.thenounproject.com"
        self._session = Session()
    
    def set_api_key(self, key: str) -> None:
        """
        Sets API key.

        :param key: The API key from the TheNounProject API.
        :type key: str
        """
        self.api_key = key

    @property
    def api_key(self) -> str:
        """
        Getter for api_key property.

        :returns: The API key from the TheNounProject API.
        :rtype: str
        """
        return self._api_key

    @api_key.setter
    def api_key(self, key: str) -> None:
        """
        Setter for api_key property.

        :param key: The API key from the TheNounProject API.
        :type key: str
        """
        self._api_key = key
    
    def set_secret_key(self, secret: str) -> None:
        """
        Sets API secret.

        :param secret: The secret key from the TheNounProject API
        :type secret: str
        """
        self.secret_key = secret

    @property
    def secret_key(self) -> str:
        """
        Getter for secret_key property.

        :returns: The secret key from the TheNounProject API.
        :rtype: str
        """
        return self._secret_key
    
    @secret_key.setter
    def secret_key(self, secret: str) -> None:
        """
        Setter for secret_key property.

        :param secret: The secret key from the TheNounProject API.
        :type secret: str
        """
        self._secret_key = secret

    def _get_oauth(self) -> OAuth1:
        """
        Returns an OAuth object using this object's API and secret key.
        Asserts that both api and secret keys have been set. 

        :raise AssertionError: Raises exception when api or secret keys have not been set.
        """
        assert isinstance(self.api_key, str), "Please set your API Key"
        assert isinstance(self.secret_key, str), "Please set your API Secret"
        return OAuth1(self.api_key, self.secret_key)

    def _get(self, url: requests.PreparedRequest) -> requests.Response:
        #TODO
        return self._session.send(url, timeout=self.timeout)

    def _get_url(self, url: str, params:dict = None) -> requests.PreparedRequest:
        """
        Returns a PreparedRequest object for a GET request, for the given URL, 
        with the given parameters, with authentication.

        :param url: The URL of the requested endpoint.
        :type url: str
        :param params: The parameters to be added onto the string. (defaults to None)
        :type params: dict

        :returns: A PreparedRequest object.
        :rtype: requests.PreparedRequest 
        """
        if self._session.auth is None:
            self._session.auth = self._get_oauth()
        req = Request("GET", url, params=params)
        return self._session.prepare_request(req)

    def _lop_assert(self, limit, offset, page) -> None:
        """
        Asserts that limit, offset and page parameters are of the correct types.

        :param limit: Limit parameter to be used as a parameter in the URL request.
        :param offset: Offset parameter to be used as a parameter in the URL request.
        :param page: Page parameter to be used as a parameter in the URL request.

        :raise AssertionError: Raises exception when limit, offset or page are not of NoneType or integer type.
        """
        NoneType = type(None)

        assert isinstance(limit, (NoneType, int)), "limit argument must be an integer"
        assert isinstance(offset, (NoneType, int)), "offset argument must be an integer"
        assert isinstance(page, (NoneType, int)), "page argument must be an integer"

    def _id_assert(self, _id:int) -> None:
        """
        Asserts that the _id parameter is positive.

        :param _id: Id of which we want to make sure it is positive.
        :type _id: int

        :raise AssertionError: Raises exception when _id is not positive.
        """
        assert _id > 0, "id argument must be positive"

    def _slug_assert(self, slug: str) -> None:
        """
        Asserts that slug is nonempty, ascii, and does not contain spaces.

        :param slug: String slug parameter to be used as a parameter in the URL request.
        :type slug: str

        :raise AssertionError: Raises exception when slug is empty, contains non-ascii characters, or contains spaces.
        """
        assert len(slug) > 0, "slug argument may not be empty"
        assert slug.isascii(), "slug argument must contain ascii characters only"
        assert slug.find(" ") == -1, "slug argument may not be multiple words"

    def _term_assert(self, term:str) -> None:
        """
        Asserts that term is nonempty.

        :param term: String term parameter to be used as a parameter in the URL request.
        :type term: str

        :raise AssertionError: Raises exception when term has a length of 0.
        """
        assert len(term) > 0, "term argument may not be empty"

    @get_endpoint
    def get_collection_icons_by_id(self, _id: int, limit:int = None, offset:int = None, page:int = None):
        """
        Fetches collection icons by id from the API.

        :param _id: Collection id.
        :type _id: int
        :param limit: Maximum number of results. (defaults to None)
        :type limit: int
        :param offset: Number of results to displace or skip over. (defaults to None)
        :type offset: int
        :param page: Number of results of limit length to displace or skip over. (defaults to None)
        :type page: int

        :raise AssertionError: Raises exception when id is nonpositive.

        :returns: TODO (Also -> ...)
        :rtype: TODO
        """
        assert isinstance(_id, int), "id argument must be an integer."
        self._lop_assert(limit, offset, page)
        params = {'limit': limit, 'offset': offset, 'page': page}
        return self._get_url(f"{self._base_url}/collection/{_id}/icons", params=params)
    
    @get_endpoint
    def get_collection_icons_by_slug(self, slug: str, limit:int = None, offset:int = None, page:int = None):
        """
        Fetches collection icons by slug from the API.

        :param slug: Collection slug.
        :type slug: str
        :param limit: Maximum number of results. (defaults to None)
        :type limit: int
        :param offset: Number of results to displace or skip over. (defaults to None)
        :type offset: int
        :param page: Number of results of limit length to displace or skip over. (defaults to None)
        :type page: int

        :raise AssertionError: Raises exception when slug is an empty string, contains non ascii characters or contains multiple words.

        :returns: TODO (Also -> ...)
        :rtype: TODO
        """
        assert isinstance(slug, str), "slug argument must be a string."
        self._lop_assert(limit, offset, page)
        self._slug_assert(slug)
        params = {'limit': limit, 'offset': offset, 'page': page}
        return self._get_url(f"{self._base_url}/collection/{slug}/icons", params=params)

    @methoddispatch
    def get_collection_icons(self, identifier: Union[int, str], limit:int = None, offset:int = None, page:int = None):
        """
        Fetches collection icons, either by id or by slug.

        :param identifier: Collection identifier (id or slug).
        :type identifier: Union[int, str]
        :param limit: Maximum number of results. (defaults to None)
        :type limit: int
        :param offset: Number of results to displace or skip over. (defaults to None)
        :type offset: int
        :param page: Number of results of limit length to displace or skip over. (defaults to None)
        :type page: int

        :raise AssertionError: Raises exception when identifier is a nonpositive integer or a string that's empty, non-ascii or with multiple words.

        :returns: TODO (Also -> ...)
        :rtype: TODO
        """
        raise AssertionError("Argument must be an integer id, or a string slug.")

    @get_collection_icons.register(int)
    @get_endpoint
    def _(self, _id: int, limit:int = None, offset:int = None, page:int = None):
        """
        This method is the implementation of get_collection_icons, in the case that the identifier is an integer.
        """
        return self.get_collection_icons_by_id(_id, limit, offset, page)
    
    @get_collection_icons.register(str)
    @get_endpoint
    def _(self, slug: str, limit:int = None, offset:int = None, page:int = None):
        """
        This method is the implementation of get_collection_icons, in the case that the identifier is a string.
        """
        return self.get_collection_icons_by_slug(slug, limit, offset, page)

    @get_endpoint
    def get_collection_by_id(self, _id: int):
        """
        Fetches a single collection by id.

        :param _id: Collection ID.
        :type _id: int

        :raise AssertionError: Raises exception when id is nonpositive.

        :returns: TODO (Also -> ...)
        :rtype: TODO
        """
        assert isinstance(_id, int), "id argument must be an integer."
        self._id_assert(_id)
        return self._get_url(f"{self._base_url}/collection/{_id}")
    
    @get_endpoint
    def get_collection_by_slug(self, slug: str):
        """
        Fetches a single collection by slug.

        :param slug: Collection slug.
        :type slug: str

        :raise AssertionError: Raises exception when slug is an empty string, contains non ascii characters or contains multiple words.

        :returns: TODO (Also -> ...)
        :rtype: TODO
        """
        assert isinstance(slug, str), "slug argument must be a string."
        self._slug_assert(slug)
        return self._get_url(f"{self._base_url}/collection/{slug}")

    @methoddispatch
    def get_collection(self, identifier: Union[int, str]):
        """
        Fetches single collections, either by id or by slug.

        :param identifier: Collection identifier (id or slug).
        :type identifier: Union[int, str]

        :raise AssertionError: Raises exception when identifier is a nonpositive integer or a string that's empty, non-ascii or with multiple words.

        :returns: TODO (Also -> ...)
        :rtype: TODO
        """
        raise AssertionError("Argument must be an integer id, or a string slug.")

    @get_collection.register(int)
    @get_endpoint
    def _(self, _id: int):
        """
        This method is the implementation of get_collection, in the case that the identifier is an integer.
        """
        return self.get_collection_by_id(_id)
    
    @get_collection.register(str)
    @get_endpoint
    def _(self, slug: str):
        """
        This method is the implementation of get_collection, in the case that the identifier is a string.
        """
        return self.get_collection_by_slug(slug)

    @get_endpoint
    def get_icon_by_id(self, _id: int):
        """
        Fetches a single icon by id.

        :param _id: Icon id.
        :type _id: int

        :raise AssertionError: Raises exception when id is nonpositive.

        :returns: TODO (Also -> ...)
        :rtype: TODO
        """
        assert isinstance(_id, int), "id argument must be an integer."
        self._id_assert(_id)
        return self._get_url(f"{self._base_url}/icon/{_id}")
    
    @get_endpoint
    def get_icon_by_term(self, term: str):
        """
        Fetches a single icon by term.

        :param term: Icon term.
        :type term: str

        :raise AssertionError: Raises exception when term is an empty string.

        :returns: TODO (Also -> ...)
        :rtype: TODO
        """
        assert isinstance(term, str), "term argument must be a string."
        self._term_assert(term)
        return self._get_url(f"{self._base_url}/icon/{term}")

    @methoddispatch
    def get_icon(self, identifier: Union[int, str]):
        """
        Fetches single icon, either by id or by term.

        :param identifier: Collection identifier (id or term).
        :type identifier: Union[int, str]

        :raise AssertionError: Raises exception when identifier is a nonpositive integer or an empty string.

        :returns: TODO (Also -> ...)
        :rtype: TODO
        """
        raise AssertionError("Argument must be an integer id, or a string term.")

    @get_icon.register(int)
    @get_endpoint
    def _(self, _id: int):
        """
        This method is the implementation of get_icon, in the case that the identifier is an integer.
        """
        return self.get_icon_by_id(_id)
    
    @get_icon.register(str)
    def _(self, term: str):
        """
        This method is the implementation of get_icon, in the case that the identifier is a string.
        """
        return self.get_icon_by_term(term)

    @get_endpoint
    def get_recent_icons(self, limit:int = None, offset:int = None, page:int = None):
        """
        Fetches recent icons.

        :param limit: Maximum number of results. (defaults to None)
        :type limit: int
        :param offset: Number of results to displace or skip over. (defaults to None)
        :type offset: int
        :param page: Number of results of limit length to displace or skip over. (defaults to None)
        :type page: int

        :returns: TODO (Also -> ...)
        :rtype: TODO
        """
        self._lop_assert(limit, offset, page)
        params = {'limit': limit, 'offset': offset, 'page': page}
        return self._get_url(f"{self._base_url}/icons/recent_uploads", params=params)
    
    @get_endpoint
    def get_icons_by_term(self, term: str, public_domain_only: Union[bool, int] = False, limit:int = None, offset:int = None, page:int = None):
        """
        Fetches a list of icons by term.

        :param term: Collection term.
        :type term: str
        :param public_domain_only: Limit results to public domain icons only (defaults to False)
        :type term: Union[bool, int]
        :param limit: Maximum number of results. (defaults to None)
        :type limit: int
        :param offset: Number of results to displace or skip over. (defaults to None)
        :type offset: int
        :param page: Number of results of limit length to displace or skip over. (defaults to None)
        :type page: int

        :raise AssertionError: Raises exception when term is an empty string.

        :returns: TODO (Also -> ...)
        :rtype: TODO
        """
        assert isinstance(term, str), "term argument must be a string."
        assert isinstance(public_domain_only, (bool, int)), "public_domain_only argument must be boolean or integer (0 for false, other for true)."
        self._lop_assert(limit, offset, page)
        self._term_assert(term)
        params = {'limit_to_public_domain': int(public_domain_only), 'limit': limit, 'offset': offset, 'page': page}
        return self._get_url(f"{self._base_url}/icons/{term}", params=params)

    @get_endpoint
    def get_usage(self):
        """
        Fetches current oauth usage and limits.

        :returns: TODO (Also -> ...)
        :rtype: TODO
        """
        return self._get_url(f"{self._base_url}/oauth/usage")

    @get_endpoint
    def get_user_collection(self, user_id: int, slug: str):
        """
        Fetches a single collection associated with a user.

        :param user_id: User id.
        :type user_id: int
        :param slug: Collection slug.
        :type slug: str

        :raise AssertionError: Raises exception when user_id is not positive, or when slug is an empty string, contains non ascii characters or contains multiple words.

        :returns: TODO (Also -> ...)
        :rtype: TODO
        """
        assert isinstance(user_id, int), "user_id argument must be an integer."
        assert isinstance(slug, str), "slug argument must be a string."
        self._id_assert(user_id)
        self._slug_assert(slug)
        return self._get_url(f"{self._base_url}/user/{user_id}/collections/{slug}")
    
    @get_endpoint
    def get_user_collections(self, user_id: int):
        """
        Fetches a list of collections associated with a user.

        :param user_id: User id.
        :type user_id: int

        :raise AssertionError: Raises exception when user_id is not positive.

        :returns: TODO (Also -> ...)
        :rtype: TODO
        """
        assert isinstance(user_id, int), "user_id argument must be an integer."
        self._id_assert(user_id)
        return self._get_url(f"{self._base_url}/user/{user_id}/collections")
    
    @get_endpoint
    def get_user_uploads(self, username: str, limit:int = None, offset:int = None, page:int = None):
        """
        Fetches a list of uploads associated with a user.

        :param username: Username.
        :type username: str
        :param public_domain_only: Limit results to public domain icons only (defaults to False)
        :type term: Union[bool, int]
        :param limit: Maximum number of results. (defaults to None)
        :type limit: int
        :param offset: Number of results to displace or skip over. (defaults to None)
        :type offset: int
        :param page: Number of results of limit length to displace or skip over. (defaults to None)
        :type page: int

        :returns: TODO (Also -> ...)
        :rtype: TODO
        """
        assert isinstance(username, str), "username argument must be a string."
        self._lop_assert(limit, offset, page)
        params = {'limit': limit, 'offset': offset, 'page': page}
        return self._get_url(f"{self._base_url}/user/{username}/uploads", params=params)

def main():
    from pprint import pprint
    import keys
    key, secret = keys.get()
    tnp = TheNounProject(key, secret)
    response = tnp.get_collection_by_id(12)
    pprint(response)
    breakpoint()

if __name__ == "__main__":
    main()

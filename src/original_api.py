
import requests, json
from requests import Request, Session
from requests_oauthlib import OAuth1
from functools import wraps, singledispatch, update_wrapper
from typing import Union, List

from exceptions import STATUS_CODE_EXCEPTIONS

from models import Collection, Collections, Icon, Icons, Usage, Publish

class Call:
    @staticmethod
    
    def dispatch(f):
        # Modified version of singledispatch to work with methods
        dispatcher = singledispatch(f)
        def wrapper(*args, **kw):
            return dispatcher.dispatch(args[1].__class__)(*args, **kw)
        wrapper.register = dispatcher.register
        update_wrapper(wrapper, f)
        return wrapper

    @staticmethod
    def _get_endpoint(model_class, method: str, f):

        @wraps(f)
        def wrapper(self, *args, **kwargs):
            self._method = method

            prepared_request = f(self, *args, **kwargs)
            if self._testing:
                return prepared_request

            response = self._send(prepared_request)

            if response.status_code in STATUS_CODE_EXCEPTIONS:
                print(response.text)
                print(response.url)
                breakpoint()
                raise STATUS_CODE_EXCEPTIONS[response.status_code](response)

            json_data = response.json()

            model = model_class()
            return model.parse(json_data)
        
        return wrapper
    
    collection  = lambda f, method="GET", model_class=Collection: Call._get_endpoint(model_class, method, f)
    collections = lambda f, method="GET", model_class=Collections: Call._get_endpoint(model_class, method, f)
    icon        = lambda f, method="GET", model_class=Icon: Call._get_endpoint(model_class, method, f)
    icons       = lambda f, method="GET", model_class=Icons: Call._get_endpoint(model_class, method, f)
    usage       = lambda f, method="GET", model_class=Usage: Call._get_endpoint(model_class, method, f)
    publish     = lambda f, method="POST", model_class=Publish: Call._get_endpoint(model_class, method, f)

"""
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
        return f"
    <APIResponse [{self.status_code}] on url {self.response.url}>"
    
    def __repr__(self):
        return f"<APIResponse [{self.status_code}] on url {self.response.url}>"
    
    def __getitem__(self, item):
        if self.json is None:
            raise Exception("Response did not contain JSON, likely due to a request error. It's recommended to check the status_code before accessing this field.")
            
        return self.json[item]
"""

class API:
    """
    API is a class allowing convenient access to the TheNounProject API.
    """

    def __init__(self, key:str = None, secret:str = None, testing:bool = False, timeout:Union[int, tuple, None] = 5):
        """
        Construct a new 'API' object.

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
        self._testing = testing
        self._timeout = timeout
        
        self._method = "GET"
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
        Asserts that both api and secret keys have been set. 

        :raise AssertionError: Raises exception when api or secret keys have not been set.

        :returns: Returns an OAuth object using this object's API and secret key.
        :rtype: OAuth1
        """
        assert isinstance(self.api_key, str), "Please set your API Key"
        assert isinstance(self.secret_key, str), "Please set your API Secret"
        return OAuth1(self.api_key, self.secret_key)

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
        Returns a PreparedRequest object for a GET request, for the given URL, 
        with the given parameters, with authentication.

        :param url: The URL of the requested endpoint.
        :type url: str
        :param method: The request method. Eg: GET, POST.
        :type method: str
        :param params: The parameters to be added onto the string.
        :type params: dict

        :returns: A PreparedRequest object.
        :rtype: requests.PreparedRequest 
        """
        if self._session.auth is None:
            self._session.auth = self._get_oauth()
        req = Request(self._method, url, **{"params" if self._method == "GET" else "json": params})
        return self._session.prepare_request(req)
    
    def _lop_assert(self, limit, offset, page) -> None:
        """
        Asserts that limit, offset and page parameters are all integers.

        :param limit: Limit parameter to be used as a parameter in the URL request.
        :param offset: Offset parameter to be used as a parameter in the URL request.
        :param page: Page parameter to be used as a parameter in the URL request.

        :raise AssertionError: Raises exception when limit, offset or page are not of NoneType or integer type.
        """
        NoneType = type(None)

        assert isinstance(limit, (NoneType, int)), "limit argument must be an integer"
        assert isinstance(offset, (NoneType, int)), "offset argument must be an integer"
        assert isinstance(page, (NoneType, int)), "page argument must be an integer"

    def _id_assert(self, _id: int) -> None:
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

    @Call.icons
    def get_collection_icons_by_id(self, _id: int, limit:int = None, offset:int = None, page:int = None) -> List[Icon]:
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

        :returns: List of Icon objects from the collection identified by the _id. 
        :rtype: List[Icon]
        """
        assert isinstance(_id, int), "id argument must be an integer."
        self._lop_assert(limit, offset, page)
        return self._prepare_url(f"{self._base_url}/collection/{_id}/icons", limit=limit, offset=offset, page=page)
    
    @Call.icons
    def get_collection_icons_by_slug(self, slug: str, limit:int = None, offset:int = None, page:int = None) -> List[Icon]:
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

        :returns: List of Icon objects from the collection identified by the slug. 
        :rtype: List[Icon]
        """
        assert isinstance(slug, str), "slug argument must be a string."
        self._lop_assert(limit, offset, page)
        self._slug_assert(slug)
        return self._prepare_url(f"{self._base_url}/collection/{slug}/icons", limit=limit, offset=offset, page=page)

    @Call.dispatch
    def get_collection_icons(self, identifier: Union[int, str], limit:int = None, offset:int = None, page:int = None) -> List[Icon]:
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

        :returns: List of Icon objects from the collection identified by the identifier. 
        :rtype: List[Icon]
        """
        raise AssertionError("Argument must be an integer id, or a string slug.")

    @get_collection_icons.register(int)
    def _(self, _id: int, limit:int = None, offset:int = None, page:int = None) -> List[Icon]:
        """
        This method is the implementation of get_collection_icons, in the case that the identifier is an integer.
        """
        return self.get_collection_icons_by_id(_id, limit, offset, page)
    
    @get_collection_icons.register(str)
    def _(self, slug: str, limit:int = None, offset:int = None, page:int = None) -> List[Icon]:
        """
        This method is the implementation of get_collection_icons, in the case that the identifier is a string.
        """
        return self.get_collection_icons_by_slug(slug, limit, offset, page)

    @Call.collection
    def get_collection_by_id(self, _id: int) -> Collection:
        """
        Fetches a single collection by id.

        :param _id: Collection ID.
        :type _id: int

        :raise AssertionError: Raises exception when id is nonpositive.

        :returns: Collection object identified by the _id.
        :rtype: Collection
        """
        assert isinstance(_id, int), "id argument must be an integer."
        self._id_assert(_id)
        return self._prepare_url(f"{self._base_url}/collection/{_id}")
    
    @Call.collection
    def get_collection_by_slug(self, slug: str) -> Collection:
        """
        Fetches a single collection by slug.

        :param slug: Collection slug.
        :type slug: str

        :raise AssertionError: Raises exception when slug is an empty string, contains non ascii characters or contains multiple words.

        :returns: Collection object identified by the slug.
        :rtype: Collection
        """
        assert isinstance(slug, str), "slug argument must be a string."
        self._slug_assert(slug)
        return self._prepare_url(f"{self._base_url}/collection/{slug}")

    @Call.dispatch
    def get_collection(self, identifier: Union[int, str]) -> Collection:
        """
        Fetches single collections, either by id or by slug.

        :param identifier: Collection identifier (id or slug).
        :type identifier: Union[int, str]

        :raise AssertionError: Raises exception when identifier is a nonpositive integer or a string that's empty, non-ascii or with multiple words.

        :returns: Collection object identified by the identifier.
        :rtype: Collection
        """
        raise AssertionError("Argument must be an integer id, or a string slug.")

    @get_collection.register(int)
    def _(self, _id: int) -> Collection:
        """
        This method is the implementation of get_collection, in the case that the identifier is an integer.
        """
        return self.get_collection_by_id(_id)
    
    @get_collection.register(str)
    def _(self, slug: str) -> Collection:
        """
        This method is the implementation of get_collection, in the case that the identifier is a string.
        """
        return self.get_collection_by_slug(slug)

    @Call.collections
    def get_collections(self, limit:int = None, offset:int = None, page:int = None) -> List[Collection]:
        """
        Fetches a list of all collections.

        :param limit: Maximum number of results. (defaults to None)
        :type limit: int
        :param offset: Number of results to displace or skip over. (defaults to None)
        :type offset: int
        :param page: Number of results of limit length to displace or skip over. (defaults to None)
        :type page: int

        :returns: List of Collection objects.
        :rtype: List[Collection]
        """
        self._lop_assert(limit, offset, page)
        return self._prepare_url(f"{self._base_url}/collections", limit=limit, offset=offset, page=page)

    @Call.icon
    def get_icon_by_id(self, _id: int) -> Icon:
        """
        Fetches a single icon by id.

        :param _id: Icon id.
        :type _id: int

        :raise AssertionError: Raises exception when id is nonpositive.

        :returns: Icon object identified by the _id.
        :rtype: Icon
        """
        assert isinstance(_id, int), "id argument must be an integer."
        self._id_assert(_id)
        return self._prepare_url(f"{self._base_url}/icon/{_id}")
    
    @Call.icon
    def get_icon_by_term(self, term: str) -> Icon:
        """
        Fetches a single icon by term.

        :param term: Icon term.
        :type term: str

        :raise AssertionError: Raises exception when term is an empty string.

        :returns: Icon object identified by the term.
        :rtype: Icon
        """
        assert isinstance(term, str), "term argument must be a string."
        self._term_assert(term)
        return self._prepare_url(f"{self._base_url}/icon/{term}")

    @Call.dispatch
    def get_icon(self, identifier: Union[int, str]) -> Icon:
        """
        Fetches single icon, either by id or by term.

        :param identifier: Collection identifier (id or term).
        :type identifier: Union[int, str]

        :raise AssertionError: Raises exception when identifier is a nonpositive integer or an empty string.

        :returns: Icon object identified by the identifier.
        :rtype: Icon
        """
        raise AssertionError("Argument must be an integer id, or a string term.")

    @get_icon.register(int)
    def _(self, _id: int) -> Icon:
        """
        This method is the implementation of get_icon, in the case that the identifier is an integer.
        """
        return self.get_icon_by_id(_id)
    
    @get_icon.register(str)
    def _(self, term: str) -> Icon:
        """
        This method is the implementation of get_icon, in the case that the identifier is a string.
        """
        return self.get_icon_by_term(term)

    @Call.icons
    def get_recent_icons(self, limit:int = None, offset:int = None, page:int = None) -> List[Icon]:
        """
        Fetches recent icons.

        :param limit: Maximum number of results. (defaults to None)
        :type limit: int
        :param offset: Number of results to displace or skip over. (defaults to None)
        :type offset: int
        :param page: Number of results of limit length to displace or skip over. (defaults to None)
        :type page: int

        :returns: List of Icon objects.
        :rtype: List[Icon]
        """
        self._lop_assert(limit, offset, page)
        return self._prepare_url(f"{self._base_url}/icons/recent_uploads", limit=limit, offset=offset, page=page)
    
    @Call.icons
    def get_icons_by_term(self, term: str, public_domain_only: Union[bool, int] = False, limit:int = None, offset:int = None, page:int = None) -> List[Icon]:
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

        :returns: List of Icon objects identified by the term.
        :rtype: List[Icon]
        """
        assert isinstance(term, str), "term argument must be a string."
        assert isinstance(public_domain_only, (bool, int)), "public_domain_only argument must be boolean or integer (0 for false, other for true)."
        self._lop_assert(limit, offset, page)
        self._term_assert(term)
        return self._prepare_url(f"{self._base_url}/icons/{term}", limit_to_public_domain=int(public_domain_only), limit=limit, offset=offset, page=page)

    @Call.usage
    def get_usage(self) -> Usage:
        """
        Fetches current oauth usage and limits.

        :returns: Usage object.
        :rtype: Usage
        """
        return self._prepare_url(f"{self._base_url}/oauth/usage")

    @Call.collection
    def get_user_collection(self, user_id: int, slug: str) -> Collection:
        """
        Fetches a single collection associated with a user.

        :param user_id: User id.
        :type user_id: int
        :param slug: Collection slug.
        :type slug: str

        :raise AssertionError: Raises exception when user_id is not positive, or when slug is an empty string, contains non ascii characters or contains multiple words.

        :returns: Collection object identified by the slug, from the user identified by the user_id.
        :rtype: Collection
        """
        assert isinstance(user_id, int), "user_id argument must be an integer."
        assert isinstance(slug, str), "slug argument must be a string."
        self._id_assert(user_id)
        self._slug_assert(slug)
        return self._prepare_url(f"{self._base_url}/user/{user_id}/collections/{slug}")
    
    @Call.collections
    def get_user_collections(self, user_id: int) -> List[Collection]:
        """
        Fetches a list of collections associated with a user.

        :param user_id: User id.
        :type user_id: int

        :raise AssertionError: Raises exception when user_id is not positive.

        :returns: List of Collection objects associated with a user identified by the user_id.
        :rtype: List[Collection]
        """
        assert isinstance(user_id, int), "user_id argument must be an integer."
        self._id_assert(user_id)
        return self._prepare_url(f"{self._base_url}/user/{user_id}/collections")
    
    @Call.icons
    def get_user_uploads(self, username: str, limit:int = None, offset:int = None, page:int = None) -> List[Icon]:
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

        :returns: List of Icon objects uploaded by user identified with the user_id.
        :rtype: List[Icon]
        """
        assert isinstance(username, str), "username argument must be a string."
        self._lop_assert(limit, offset, page)
        return self._prepare_url(f"{self._base_url}/user/{username}/uploads", limit=limit, offset=offset, page=page)

    @Call.publish
    def publish(self, icons: Union[list, set, str, int], test:bool = False):
        """
        TODO
        """
        if isinstance(icons, (list, set)):
            icons = ",".join(str(icon) for icon in icons)
        elif isinstance(icons, (str, int)):
            icons = str(icons)
        else:
            raise AssertionError("icons parameter must be a string or integer, string, list or set, where each element is an icon id.")
        return self._prepare_url(f"{self._base_url}/notify/publish" + ("?test=1" if test else ""), icons=icons)

def main():
    import keys
    from pprint import pprint
    tnp = API(*keys.get(), testing=True)
    #mod = tnp.publish(set([12, 41, 14]))
    #print(mod)
    breakpoint()
    #tnp.get_collection_by_id()
    #mod = tnp.get_collection(12)
    #print(mod)
    #breakpoint()
    #mod = tnp.get_collections(limit=2)
    #print(mod)
    #breakpoint()
    #mod = tnp.get_icon(5)
    #print(mod)
    #breakpoint()
    #mod = tnp.get_collection_icons(12, limit=2)
    #print(mod)
    #breakpoint()
    #mod = tnp.get_recent_icons(limit=2)
    #print(mod)
    #breakpoint()
    #mod = tnp.get_icons_by_term("potato", limit=2)
    #print(mod)
    #breakpoint()
    #mod = tnp.get_usage()
    #print(mod)
    #breakpoint()
    #mod = tnp.get_user_collection(1, "bicycle")
    #print(mod)
    #breakpoint()
    #mod = tnp.get_user_collections(3)
    #print(mod)
    #breakpoint()
    #mod = tnp.get_user_uploads("dan")
    #print(mod)
    #breakpoint()

    """
    class test:
        @methoddispatch
        def custom_method(self, arg):
            ''' My Custom Method! '''
            print("Main")
        
        @custom_method.register
        def _(self, arg: int):
            print("int")
        
        @custom_method.register
        def _(self, arg: str):
            print("str")
        
        def __init__(self):
            print(self.custom_method(12))
            self.custom_method()
    
    test()
    """

if __name__ == "__main__":
    main()

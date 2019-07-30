from typing import Union, List

from core import Core
from call import Call
from models import IconModel

class Icons(Core):
    @Call.icons
    def get_collection_icons_by_id(self, _id: int, limit:int = None, offset:int = None, page:int = None) -> List[IconModel]:
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
    def get_collection_icons_by_slug(self, slug: str, limit:int = None, offset:int = None, page:int = None) -> List[IconModel]:
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
    def get_collection_icons(self, identifier: Union[int, str], limit:int = None, offset:int = None, page:int = None) -> List[IconModel]:
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
    def _(self, _id: int, limit:int = None, offset:int = None, page:int = None) -> List[IconModel]:
        """
        This method is the implementation of get_collection_icons, in the case that the identifier is an integer.
        """
        return self.get_collection_icons_by_id(_id, limit, offset, page)
    
    @get_collection_icons.register(str)
    def _(self, slug: str, limit:int = None, offset:int = None, page:int = None) -> List[IconModel]:
        """
        This method is the implementation of get_collection_icons, in the case that the identifier is a string.
        """
        return self.get_collection_icons_by_slug(slug, limit, offset, page)

    @Call.icons
    def get_recent_icons(self, limit:int = None, offset:int = None, page:int = None) -> List[IconModel]:
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
    def get_icons_by_term(self, term: str, public_domain_only: Union[bool, int] = False, limit:int = None, offset:int = None, page:int = None) -> List[IconModel]:
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

    @Call.icons
    def get_user_uploads(self, username: str, limit:int = None, offset:int = None, page:int = None) -> List[IconModel]:
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

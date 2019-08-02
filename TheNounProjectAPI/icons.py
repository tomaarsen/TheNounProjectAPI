
from typing import Union, List

from TheNounProjectAPI.core import Core
from TheNounProjectAPI.call import Call
from TheNounProjectAPI.models import IconModel
from TheNounProjectAPI.exceptions import IncorrectType

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

        :raise NonPositive: Raises exception when _id is nonpositive.

        :returns: List of IconModel objects from the collection identified by the _id. 
        :rtype: List[IconModel]
        """
        self._type_assert(_id, "id", int)
        self._id_assert(_id, "id")
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

        :raise IllegalSlug: Raises exception when slug is an empty string, contains non ascii characters or contains multiple words.

        :returns: List of IconModel objects from the collection identified by the slug. 
        :rtype: List[IconModel]
        """
        self._type_assert(slug, "slug", str)
        self._slug_assert(slug, "slug")
        self._lop_assert(limit, offset, page)
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

        :raise NonPositive: Raises exception when identifier is a nonpositive integer.
        :raise IllegalSlug: Raises exception when identifier is a string that's empty, non-ascii or with multiple words.

        :returns: List of IconModel objects from the collection identified by the identifier. 
        :rtype: List[IconModel]
        """
        raise IncorrectType("identifier", (int, str))

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

    @Call.icon
    def get_icon_by_id(self, _id: int) -> IconModel:
        """
        Fetches a single icon by id.

        :param _id: Icon id.
        :type _id: int

        :raise NonPositive: Raises exception when id is nonpositive.

        :returns: IconModel object identified by the _id.
        :rtype: IconModel
        """
        self._type_assert(_id, "id", int)
        self._id_assert(_id, "id")
        return self._prepare_url(f"{self._base_url}/icon/{_id}")
    
    @Call.icon
    def get_icon_by_term(self, term: str) -> IconModel:
        """
        Fetches a single icon by term.

        :param term: Icon term.
        :type term: str

        :raise IllegalTerm: Raises exception when term is an empty string.

        :returns: IconModel object identified by the term.
        :rtype: IconModel
        """
        self._type_assert(term, "term", str)
        self._term_assert(term, "term")
        return self._prepare_url(f"{self._base_url}/icon/{term}")

    @Call.dispatch
    def get_icon(self, identifier: Union[int, str]) -> IconModel:
        """
        Fetches single icon, either by id or by term.

        :param identifier: Collection identifier (id or term).
        :type identifier: Union[int, str]

        :raise NonPositive: Raises exception when identifier is a nonpositive integer.
        :raise IllegalTerm: Raises exception when identifier is an empty string.

        :returns: IconModel object identified by the identifier.
        :rtype: IconModel
        """
        raise IncorrectType("identifier", (int, str))

    @get_icon.register(int)
    def _(self, _id: int) -> IconModel:
        """
        This method is the implementation of get_icon, in the case that the identifier is an integer.
        """
        return self.get_icon_by_id(_id)
    
    @get_icon.register(str)
    def _(self, term: str) -> IconModel:
        """
        This method is the implementation of get_icon, in the case that the identifier is a string.
        """
        return self.get_icon_by_term(term)

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

        :returns: List of IconModel objects.
        :rtype: List[IconModel]
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
        :type public_domain_only: Union[bool, int]
        :param limit: Maximum number of results. (defaults to None)
        :type limit: int
        :param offset: Number of results to displace or skip over. (defaults to None)
        :type offset: int
        :param page: Number of results of limit length to displace or skip over. (defaults to None)
        :type page: int

        :raise IllegalTerm: Raises exception when term is an empty string.

        :returns: List of IconModel objects identified by the term.
        :rtype: List[IconModel]
        """
        self._type_assert(term, "term", str)
        self._type_assert(public_domain_only, "public_domain_only", (bool, int))
        self._term_assert(term, "term")
        self._lop_assert(limit, offset, page)
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

        :raise IllegalTerm: Raises exception when username is an empty string.

        :returns: List of IconModel objects uploaded by user identified with the user_id.
        :rtype: List[IconModel]
        """
        self._type_assert(username, "username", str)
        self._term_assert(username, "username")
        self._lop_assert(limit, offset, page)
        return self._prepare_url(f"{self._base_url}/user/{username}/uploads", limit=limit, offset=offset, page=page)


from typing import Union, List

from TheNounProjectAPI.core import Core
from TheNounProjectAPI.call import Call
from TheNounProjectAPI.models import CollectionModel
from TheNounProjectAPI.exceptions import IncorrectType

class Collections(Core):

    @Call.collection
    def get_collection_by_id(self, _id: int) -> CollectionModel:
        """
        Fetches a single collection by id.

        :param _id: Collection ID.
        :type _id: int

        :raise NonPositive: Raises exception when id is nonpositive.

        :returns: CollectionModel object identified by the _id.
        :rtype: CollectionModel
        """
        self._type_assert(_id, "id", int)
        self._id_assert(_id, "id")
        return self._prepare_url(f"{self._base_url}/collection/{_id}")
    
    @Call.collection
    def get_collection_by_slug(self, slug: str) -> CollectionModel:
        """
        Fetches a single collection by slug.

        :param slug: Collection slug.
        :type slug: str

        :raise IllegalSlug: Raises exception when slug is an empty string, contains non ascii characters or contains multiple words.

        :returns: CollectionModel object identified by the slug.
        :rtype: CollectionModel
        """
        self._type_assert(slug, "slug", str)
        self._slug_assert(slug, "slug")
        return self._prepare_url(f"{self._base_url}/collection/{slug}")

    @Call.dispatch
    def get_collection(self, identifier: Union[int, str]) -> CollectionModel:
        """
        Fetches single collections, either by id or by slug.

        :param identifier: Collection identifier (id or slug).
        :type identifier: Union[int, str]

        :raise NonPositive: Raises exception when identifier is a nonpositive integer.
        :raise IllegalSlug: Raises exception when identifier is a string that's empty, non-ascii or with multiple words.

        :returns: CollectionModel object identified by the identifier.
        :rtype: CollectionModel
        """
        raise IncorrectType("identifier", (int, str))

    @get_collection.register(int)
    def _(self, _id: int) -> CollectionModel:
        """
        This method is the implementation of get_collection, in the case that the identifier is an integer.
        """
        return self.get_collection_by_id(_id)
    
    @get_collection.register(str)
    def _(self, slug: str) -> CollectionModel:
        """
        This method is the implementation of get_collection, in the case that the identifier is a string.
        """
        return self.get_collection_by_slug(slug)

    @Call.collections
    def get_collections(self, limit:int = None, offset:int = None, page:int = None) -> List[CollectionModel]:
        """
        Fetches a list of all collections.

        :param limit: Maximum number of results. (defaults to None)
        :type limit: int
        :param offset: Number of results to displace or skip over. (defaults to None)
        :type offset: int
        :param page: Number of results of limit length to displace or skip over. (defaults to None)
        :type page: int

        :returns: List of CollectionModel objects.
        :rtype: List[CollectionModel]
        """
        self._lop_assert(limit, offset, page)
        return self._prepare_url(f"{self._base_url}/collections", limit=limit, offset=offset, page=page)

    @Call.collections
    def get_user_collections(self, user_id: int) -> List[CollectionModel]:
        """
        Fetches a list of collections associated with a user.

        :param user_id: User id.
        :type user_id: int

        :raise NonPositive: Raises exception when user_id is not positive.

        :returns: List of CollectionModel objects associated with a user identified by the user_id.
        :rtype: List[CollectionModel]
        """
        self._type_assert(user_id, "user_id", int)
        self._id_assert(user_id, "user_id")
        return self._prepare_url(f"{self._base_url}/user/{user_id}/collections")

    @Call.collection
    def get_user_collection(self, user_id: int, slug: str) -> CollectionModel:
        """
        Fetches a single collection associated with a user.

        :param user_id: User id.
        :type user_id: int
        :param slug: Collection slug.
        :type slug: str

        :raise NonPositive: Raises exception when user_id is not positive.
        :raise IllegalSlug: Raises exception when slug is an empty string, contains non ascii characters or contains multiple words.

        :returns: CollectionModel object identified by the slug, from the user identified by the user_id.
        :rtype: CollectionModel
        """
        self._type_assert(user_id, "user_id", int)
        self._type_assert(slug, "slug", str)
        self._id_assert(user_id, "user_id")
        self._slug_assert(slug, "slug")
        return self._prepare_url(f"{self._base_url}/user/{user_id}/collections/{slug}")
    
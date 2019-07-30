from typing import Union

from core import Core
from call import Call
from models import CollectionModel

class Collection(Core):

    @Call.collection
    def get_collection_by_id(self, _id: int) -> CollectionModel:
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
    def get_collection_by_slug(self, slug: str) -> CollectionModel:
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
    def get_collection(self, identifier: Union[int, str]) -> CollectionModel:
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

    @Call.collection
    def get_user_collection(self, user_id: int, slug: str) -> CollectionModel:
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
    
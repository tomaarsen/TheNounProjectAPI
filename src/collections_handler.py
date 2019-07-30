from typing import List

from core import Core
from call import Call
from models import CollectionModel

class Collections(Core):

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

        :returns: List of Collection objects.
        :rtype: List[Collection]
        """
        self._lop_assert(limit, offset, page)
        return self._prepare_url(f"{self._base_url}/collections", limit=limit, offset=offset, page=page)

    @Call.collections
    def get_user_collections(self, user_id: int) -> List[CollectionModel]:
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

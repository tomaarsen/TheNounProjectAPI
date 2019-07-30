
from typing import Union

from core import Core
from call import Call
from models import IconModel

class Icon(Core):
    @Call.icon
    def get_icon_by_id(self, _id: int) -> IconModel:
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
    def get_icon_by_term(self, term: str) -> IconModel:
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
    def get_icon(self, identifier: Union[int, str]) -> IconModel:
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


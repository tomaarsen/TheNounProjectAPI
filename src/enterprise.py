
from typing import Union

from src.core import Core
from src.call import Call
from src.models import EnterpriseModel
from src.exceptions import IncorrectType

class Enterprise(Core):

    @Call.enterprise
    def report_usage(self, icons: Union[list, set, str, int], test:bool = False) -> EnterpriseModel:
        """
        Accepts icon ids for reporting icon usage.

        :param icons: Icon ids.
        :type icons: Union[list, set, str, int]
        :param test: True to test endpoint without reporting data.
        :type bool:

        :returns: EnterpriseModel object based on the icon ids.
        :rtype: EnterpriseModel
        """
        if isinstance(icons, (list, set)):
            icons = ",".join(str(icon) for icon in icons)
        elif isinstance(icons, (str, int)):
            icons = str(icons)
        else:
            raise IncorrectType("icons", (list, set, str, int))
        return self._prepare_url(f"{self._base_url}/notify/publish" + ("?test=1" if test else ""), icons=icons)

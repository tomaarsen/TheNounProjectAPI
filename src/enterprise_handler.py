
from typing import Union

from core import Core
from call import Call
from models import PublishModel

class Enterprise(Core):

    @Call.publish
    def publish(self, icons: Union[list, set, str, int], test:bool = False) -> PublishModel:
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

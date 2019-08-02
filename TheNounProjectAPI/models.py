
import requests

from TheNounProjectAPI.exceptions import NotFound
from typing import Any, TypeVar, Type, Union, Tuple
   
class Model:
    """
    Model is a base class to be used as a superclass for conveniently accessing data.
    All of the json returned by the API is parsed through this model, and stored under the json attribute
    """
    def __init__(self):
        """ Constructs a new 'Model' object. """
        self._output_keys = ()
        self.json: DotDict = DotDict()
        """ The json data returned by the API, as a :class:`DotDict` instance. """
        self.response: requests.Response = None
        """ requests.Response object used to fill this Model. """
    
    @classmethod
    def parse(cls, data: dict, response:requests.Response = None):
        """ 
        Constructs and returns an instance of (sub)class, with the json attribute 
        set to a conveniently accessible `DotDict` object, filled with `data`. 
        """
        instance = cls()
        instance.json = DotDict(data)
        instance.response = response
        return instance

    def __getattr__(self, name: str):
        """ Passes model.data to model.json.data. """
        return getattr(self.json, name)

    def __getitem__(self, name: str):
        """ Passes model['data'] to model.json['data']. """
        return self.json[name]

    def __eq__(self, other: object):
        """ Checks whether all attributes of self match with other. """
        return self.json.__dict__ == other.json.__dict__

    def __repr__(self):
        """ Returns string with class name, followed by all output_keys and their values. 
            eg: <Collection: Name: Cue, Slug: cue, Id: 12> """
        return "<{}: {}>".format(self.__class__.__name__,
                                ", ".join(f"{output_key.title}: {self.json[output_key.key]}" for output_key in self._output_keys if getattr(self, output_key.key, None) is not None))

class ModelList(list):
    """
    ModelList is a base class to be used as a superclass for conveniently accessing lists of Model objects.
    """
    @classmethod
    def parse(cls, data: dict, instance_class: Model, main_keys: list, response:requests.Response = None):
        """
        Constructs and returns a list of instances of instance_class, a subclass of Model.
        In addition, this list has some additional attributes based on the data dictionary.
        """
        main_dict = [data[key] for key in main_keys if key in data][0]
        instance = cls()
        instance.extend([instance_class.parse(item) for item in main_dict])
        instance.response = response
        for key, val in data.items():
            setattr(instance, key if key not in main_keys else main_keys[0], sequence_to_dot(val))
        return instance

class CollectionModel(Model):
    """
    CollectionModel is a subclass of Model, with different attributes displayed when printed.
    See :ref:`collection-label` for more information regarding what attributes comes with this object.
    """
    def __init__(self):
        super().__init__()
        self._output_keys = (OutputKeys("name"), 
                            OutputKeys("slug"), 
                            OutputKeys("id"))
    
    @classmethod
    def parse(cls, data: dict, response:requests.Response = None):
        if "collection" in data:
            data = data["collection"]
        return super().parse(data, response)

class CollectionsModel(ModelList):
    """
    CollectionsModel is a subclass of ModelList, which focuses on turning CollectionModel objects into a list.
    See :ref:`collections-label` for more information regarding what attributes comes with this object.
    """
    @classmethod
    def parse(cls, data: dict, response:requests.Response = None):
        """
        Constructs and returns a list of CollectionModel objects.
        In addition, this list may have some additional attributes like `generated_at` based on the data dictionary.
        """
        return super().parse(data, CollectionModel, main_keys=["collections"], response=response)

class IconModel(Model):
    """
    IconModel is a subclass of Model, with different attributes displayed when printed.
    See :ref:`icon-label` for more information regarding what attributes comes with this object.
    """
    def __init__(self):
        super().__init__()
        self._output_keys = (OutputKeys("term"), 
                            OutputKeys("term_slug", "Slug"), 
                            OutputKeys("id"))
    @classmethod
    def parse(cls, data: dict, response:requests.Response = None):
        if "icon" in data:
            data = data["icon"]
        return super().parse(data, response)

class IconsModel(ModelList):
    """
    IconsModel is a subclass of ModelList, which focuses on turning IconModel objects into a list.
    See :ref:`icons-label` for more information regarding what attributes comes with this object.
    """
    @classmethod
    def parse(cls, data: dict, response:requests.Response = None):
        """
        Constructs and returns a list of IconModel objects.
        In addition, this list may have some additional attributes like `generated_at` based on the data dictionary.
        """
        return super().parse(data, IconModel, main_keys=["icons", "recent_uploads", "uploads"], response=response)

class UsageModel(Model):
    """
    UsageModel is a subclass of Model, with different attributes displayed when printed.
    See :ref:`usage-label` for more information regarding what attributes comes with this object.
    """
    def __init__(self):
        super().__init__()
        self._output_keys = (OutputKeys(("usage", "hourly"), "Hourly"), 
                            OutputKeys(("usage", "daily"), "Daily"), 
                            OutputKeys(("usage", "monthly"), "Monthly"),)
    
    def __repr__(self):
        """ Returns string with class name, followed by all output_keys and their values. 
            eg: <Collection: Name: Cue, Slug: cue, Id: 12> """
        return "<{}: {}>".format(self.__class__.__name__,
                                ", ".join(f"{output_key.title}: {self.json[output_key.key[0]][output_key.key[1]]}" for output_key in self._output_keys))

class EnterpriseModel(Model):
    """
    EnterpriseModel is a subclass of Model, with different attributes displayed when printed.
    See :ref:`enterprise-label` for more information regarding what attributes comes with this object.
    """
    def __init__(self):
        super().__init__()
        self._output_keys = (OutputKeys("licenses_consumed", "Licenses Consumed"),
                            OutputKeys("result"))

class OutputKeys:
    """
    Class to store key and title value, used for outputting attributes.
    """ 
    def __init__(self, key: Union[str, Tuple[str, ...]], title:str = None):
        """
        Constructs a 'OutputKeys' object, with a key and a title.
        """
        self.key = key
        self.title = title or key.title()

class DotDict(dict):
    """
    Subclass of dict allowing dot notation for items in the dict:

    .. code-block :: python
        :linenos:

        dot_dict.author.username 
        # is equivalent to:
        dot_dict["author"]["username"]
    """ 
    def __getattr__(self, name: str):
        """ 
        Allows dot_dict.data.more_data to be equivalent to dot_dict['data']['more_data']. 
        """
        if name not in self:
            raise AttributeError(f"Object has no attribute \'{name}\'")
        val = self.get(name)
        return sequence_to_dot(val)
    
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class DotList(list):
    """
    Subclass of list allowing dot notation for dicts that might be in the list.
    """ 
    def __getitem__(self, key: int):
        """ 
        Allows dot_dict[0][2].data to be equivalent to dot_dict[0][2]['data']. 
        """
        val = list.__getitem__(self, key)
        return sequence_to_dot(val)

def sequence_to_dot(val: Any) -> Any:
    """
    Returns DotDict of val if val is a dict.
    Returns DotList of val if val is a list.
    Otherwise returns val.
    """
    if isinstance(val, dict):
        return DotDict(val)
    if isinstance(val, list):
        return DotList(val)
    return val
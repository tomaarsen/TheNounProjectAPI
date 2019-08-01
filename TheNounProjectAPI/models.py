
import context

import requests

from TheNounProjectAPI.exceptions import NotFound
from typing import Any, TypeVar, Type, Union, Tuple

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

class DotDict(dict):
    """
    Subclass of dict allowing dot notation for items in the dict.
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

class Model:
    """
    Model is a base class to be used as a superclass for conveniently accessing data.
    """
    def __init__(self):
        """ Constructs a new 'Model' object. """
        self.output_keys = ()

        """ Main attribute to access data. Can be used both like .json.data.more_data
            and .json['data']['more_data'] """
        self.json = DotDict()
    
    @classmethod
    def parse(cls, data: dict, response:requests.Response = None):
        """ Constructs and returns an instance of (sub)class, with the json attribute 
            set to a conveniently accessible DotDict object with 'data'. """
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
                                ", ".join(f"{output_key.title}: {self.json[output_key.key]}" for output_key in self.output_keys if getattr(self, output_key.key, None) is not None))

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
            setattr(instance, key, sequence_to_dot(val))
        return instance

class CollectionModel(Model):
    """
    CollectionModel is a subclass of Model, with different attributes displayed.
    """
    def __init__(self):
        super().__init__()
        self.output_keys = (OutputKeys("name"), 
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
    """
    @classmethod
    def parse(cls, data: dict, response:requests.Response = None):
        return super().parse(data, CollectionModel, main_keys=["collections"], response=response)

class IconModel(Model):
    """
    IconModel is a subclass of Model, with different attributes displayed.
    """
    def __init__(self):
        super().__init__()
        self.output_keys = (OutputKeys("term"), 
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
    """
    @classmethod
    def parse(cls, data: dict, response:requests.Response = None):
        return super().parse(data, IconModel, main_keys=["icons", "recent_uploads", "uploads"], response=response)

class UsageModel(Model):
    """
    UsageModel is a subclass of Model, with different attributes displayed.
    """
    def __init__(self):
        super().__init__()
        self.output_keys = (OutputKeys(("usage", "hourly"), "Hourly"), 
                            OutputKeys(("usage", "daily"), "Daily"), 
                            OutputKeys(("usage", "monthly"), "Monthly"),)
    
    def __repr__(self):
        """ Returns string with class name, followed by all output_keys and their values. 
            eg: <Collection: Name: Cue, Slug: cue, Id: 12> """
        return "<{}: {}>".format(self.__class__.__name__,
                                ", ".join(f"{output_key.title}: {self.json[output_key.key[0]][output_key.key[1]]}" for output_key in self.output_keys))

class EnterpriseModel(Model):
    """
    EnterpriseModel is a subclass of Model, with different attributes displayed.
    """
    def __init__(self):
        super().__init__()
        self.output_keys = (OutputKeys("licenses_consumed", "Licenses Consumed"),
                            OutputKeys("result"))
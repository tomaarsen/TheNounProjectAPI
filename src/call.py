
import context

from functools import wraps, singledispatch, update_wrapper
from typing import Union, Callable, Type

from src.exceptions import STATUS_CODE_EXCEPTIONS
from src.models import CollectionModel, CollectionsModel, IconModel, IconsModel, UsageModel, EnterpriseModel, Model, ModelList

class Call:
    """
    Call is a class containing methods used as decorators, each helping with making the actual requests to the TheNounProject API.
    """

    @staticmethod
    def dispatch(f: Callable) -> Callable:
        """
        This method allows the use of singledispatch on methods, 
        a feature that will be implemented in functools in Python 3.8.x in the future.

        :param f: The decorated method.
        :type f: Callable

        :returns: Decorator method which takes the type of the second parameter instead of the first, 
                  as the first is self in a method, and passes this type on to the dispatcher.
        :rtype: Callable
        """
        dispatcher = singledispatch(f)
        def wrapper(*args, **kwargs):
            return dispatcher.dispatch(args[1].__class__)(*args, **kwargs)
        wrapper.register = dispatcher.register
        update_wrapper(wrapper, f)
        return wrapper

    @staticmethod
    def _get_endpoint(model_class: Union[Type[Model], Type[ModelList]], method: str, f: Callable) -> Callable:
        """
        Returns wrapper which receives a requests.PreparedRequests, 
        sends this request, checks for exceptions, and returns the json parsed through the correct model.

        :param model_class: The class of the model to use for the output data.
        :type model_class: Union[Type[Model], Type[ModelList]]
        :param method: String form of which method to use. Either "GET" or "POST".
        :type method: str
        :param f: The decorated method. 
        :type f: Callable

        :returns: Decorator function.
        :rtype: Callable
        """
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            self._method = method

            prepared_request = f(self, *args, **kwargs)
            if self._testing:
                return prepared_request

            response = self._send(prepared_request)

            if response.status_code in STATUS_CODE_EXCEPTIONS:
                print(response.text)
                print(response.url)
                breakpoint()
                raise STATUS_CODE_EXCEPTIONS[response.status_code](response)

            json_data = response.json()

            model = model_class()
            return model.parse(json_data)
        
        return wrapper
    
    """
    Some lambda functions, where the method and model_class are already determined.
    This allows me to write @Call.collection instead of @Call._get_endpoint(method="GET", model_class=CollectionModel),
    which also requires more imports in other files.
    """
    collection  = lambda f, method="GET", model_class=CollectionModel: Call._get_endpoint(model_class, method, f)
    collections = lambda f, method="GET", model_class=CollectionsModel: Call._get_endpoint(model_class, method, f)
    icon        = lambda f, method="GET", model_class=IconModel: Call._get_endpoint(model_class, method, f)
    icons       = lambda f, method="GET", model_class=IconsModel: Call._get_endpoint(model_class, method, f)
    usage       = lambda f, method="GET", model_class=UsageModel: Call._get_endpoint(model_class, method, f)
    enterprise  = lambda f, method="POST", model_class=EnterpriseModel: Call._get_endpoint(model_class, method, f)

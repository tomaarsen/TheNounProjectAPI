
from functools import singledispatch
import wrapt
from typing import Union, Callable, Type, List

from TheNounProjectAPI.exceptions import STATUS_CODE_EXCEPTIONS, STATUS_CODE_SUCCESS, UnknownStatusCode
from TheNounProjectAPI.models import CollectionModel, CollectionsModel, IconModel, IconsModel, UsageModel, EnterpriseModel, Model, ModelList

class Call:
    """
    Call is a class containing methods used as decorators, each helping with making the actual requests to the TheNounProject API.
    """

    @staticmethod
    def dispatch(f: Callable) -> Callable:
        """
        This method allows the use of singledispatch on methods, 
        a feature that will be implemented in functools in Python 3.8.x+ in the future.

        :param f: The decorated method.
        :type f: Callable

        :returns: Decorator method which takes the type of the second parameter instead of the first, 
                  as the first is self in a method, and passes this type on to the dispatcher.
        :rtype: Callable
        """
        dispatcher = singledispatch(f)
        @wrapt.decorator
        def wrapper(wrapped, instance=None, args=(), kwargs={}):
            return dispatcher.dispatch(args[0].__class__)(instance, *args, **kwargs)
        out = wrapper(f)
        out.register = dispatcher.register
        return out

    @staticmethod
    def _get_endpoint(model_class: Union[Type[Model], Type[ModelList]], method: str) -> Callable:
        """
        Returns wrapper which receives a requests.PreparedRequests, 
        sends this request, checks for exceptions, and returns the json parsed through the correct model.

        :param model_class: The class of the model to use for the output data.
        :type model_class: Union[Type[Model], Type[ModelList]]
        :param method: String form of which method to use. Either "GET" or "POST".
        :type method: str

        :returns: Decorator function.
        :rtype: Callable
        """
        @wrapt.decorator
        def wrapper(wrapped, instance=None, args=(), kwargs={}) -> Union[Model, List[Model]]:
            # Set method for API instance.
            instance._method = method

            # Call the decorated function with the args and kwargs.
            # All of the decorated functions return a PreparedRequest which we will use.
            prepared_request = wrapped(*args, **kwargs)
            # If testing is true, then we want to simply return this PreparedRequest. This is useful for testing only.
            if instance._testing:
                return prepared_request

            # Send the PreparedRequest, and get the response
            response = instance._send(prepared_request)

            # If status_code indicates success
            if response.status_code in STATUS_CODE_SUCCESS:
                # Parse as JSON, get model, parse json in terms of the model
                json_data = response.json()
                model = model_class()
                return model.parse(json_data, response)
            # If status_code indicates an error we know
            elif response.status_code in STATUS_CODE_EXCEPTIONS:
                raise STATUS_CODE_EXCEPTIONS[response.status_code](response)
            # If status_code is a code we don't have a proper exception/response for.
            else:
                raise UnknownStatusCode(response)
        
        return wrapper
    
    """
    Some lambda functions, where the method and model_class are already determined.
    This allows me to write @Call.collection instead of @Call._get_endpoint(method="GET", model_class=CollectionModel),
    which also requires more imports in other files.
    """
    collection  = lambda f, method="GET", model_class=CollectionModel: Call._get_endpoint(model_class, method)(f)
    collections = lambda f, method="GET", model_class=CollectionsModel: Call._get_endpoint(model_class, method)(f)
    icon        = lambda f, method="GET", model_class=IconModel: Call._get_endpoint(model_class, method)(f)
    icons       = lambda f, method="GET", model_class=IconsModel: Call._get_endpoint(model_class, method)(f)
    usage       = lambda f, method="GET", model_class=UsageModel: Call._get_endpoint(model_class, method)(f)
    enterprise  = lambda f, method="POST", model_class=EnterpriseModel: Call._get_endpoint(model_class, method)(f)

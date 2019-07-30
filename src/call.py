
from functools import wraps, singledispatch, update_wrapper

from src.exceptions import STATUS_CODE_EXCEPTIONS
from models import CollectionModel, CollectionsModel, IconModel, IconsModel, UsageModel, PublishModel

class Call:

    @staticmethod
    def dispatch(f):
        # Modified version of singledispatch to work with methods
        dispatcher = singledispatch(f)
        def wrapper(*args, **kw):
            return dispatcher.dispatch(args[1].__class__)(*args, **kw)
        wrapper.register = dispatcher.register
        update_wrapper(wrapper, f)
        return wrapper

    @staticmethod
    def _get_endpoint(model_class, method: str, f):

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
    
    collection  = lambda f, method="GET", model_class=CollectionModel: Call._get_endpoint(model_class, method, f)
    collections = lambda f, method="GET", model_class=CollectionsModel: Call._get_endpoint(model_class, method, f)
    icon        = lambda f, method="GET", model_class=IconModel: Call._get_endpoint(model_class, method, f)
    icons       = lambda f, method="GET", model_class=IconsModel: Call._get_endpoint(model_class, method, f)
    usage       = lambda f, method="GET", model_class=UsageModel: Call._get_endpoint(model_class, method, f)
    publish     = lambda f, method="POST", model_class=PublishModel: Call._get_endpoint(model_class, method, f)

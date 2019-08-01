
import context

from TheNounProjectAPI.collections import Collections
from TheNounProjectAPI.icons import Icons
from TheNounProjectAPI.usage import Usage
from TheNounProjectAPI.enterprise import Enterprise

class API(Collections, Icons, Usage, Enterprise):
    """
    API is a class allowing convenient access to the TheNounProject API.
    """
    pass

def main():
    from api_keys import get
    api = API(*get())
    #help(api)
    breakpoint()

if __name__ == "__main__":
    main()
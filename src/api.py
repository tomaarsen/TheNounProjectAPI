
import context

from src.collections import Collections
from src.icons import Icons
from src.usage import Usage
from src.enterprise import Enterprise

class API(Collections, Icons, Usage, Enterprise):
    """
    API is a class allowing convenient access to the TheNounProject API.
    """
    pass

def main():
    from api_keys import get
    api = API(*get())
    breakpoint()

if __name__ == "__main__":
    main()
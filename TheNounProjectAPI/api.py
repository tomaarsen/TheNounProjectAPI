
import os, sys
""" Expand the context so we can easily access TheNounProjectAPI """
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from TheNounProjectAPI.collections import Collections
from TheNounProjectAPI.icons import Icons
from TheNounProjectAPI.usage import Usage
from TheNounProjectAPI.enterprise import Enterprise

class API(Collections, Icons, Usage, Enterprise):
    """
    API is a class allowing convenient access to the TheNounProject API.
    """
    pass

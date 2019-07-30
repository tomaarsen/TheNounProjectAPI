
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.collections import Collections
from src.icons import Icons
from src.usage import Usage
from src.enterprise import Enterprise

class API(Collections, Icons, Usage, Enterprise):
    pass

"""
def main():
    api = API()

if __name__ == "__main__":
    main()
"""
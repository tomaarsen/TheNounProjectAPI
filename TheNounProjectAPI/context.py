
import os, sys
''' Expand the context so we can easily import using 'import TheNounProjectAPI.<file>' '''
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest

import context 

from src.api import API
from src.exceptions import IllegalTerm

class TermAssert(unittest.TestCase):

    def setUp(self):
        key = "mock api key to satisfy type check in tnp._get_oauth()"
        secret = "mock secret key to satisfy type check in tnp._get_oauth()"
        self.tnp = API(key, secret, testing=True)

    def test_str(self):
        """
        Test _term_assert with term "goat"
        """
        term = "goat"
        self.tnp._term_assert(term, "term")
 
    def test_str_non_ascii(self):
        """
        Test _term_assert with term "¤"
        """
        term = "¤"
        self.tnp._term_assert(term, "term")
 
    def test_str_multiple_words(self):
        """
        Test _term_assert with term "goat horn"
        """
        term = "goat horn"
        self.tnp._term_assert(term, "term")

    def test_str_empty(self):
        """
        Test _term_assert with illegal term ""
        """
        term = ""
        with self.assertRaises(IllegalTerm):
            self.tnp._term_assert(term, "term")

if __name__ == "__main__":
    unittest.main()
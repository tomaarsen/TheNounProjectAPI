import unittest

import context 


from src.api import API

class SlugAssert(unittest.TestCase):

    def setUp(self):
        key = "mock api key to satisfy type check in tnp._get_oauth()"
        secret = "mock secret key to satisfy type check in tnp._get_oauth()"
        self.tnp = API(key, secret, testing=True)

    def test_str(self):
        """
        Test _slug_assert with slug "goat"
        """
        slug = "goat"
        self.tnp._slug_assert(slug)
    
    def test_str_empty(self):
        """
        Test _slug_assert with illegal slug ""
        """
        slug = ""
        with self.assertRaises(AssertionError):
            self.tnp._slug_assert(slug)
 
    def test_str_non_ascii(self):
        """
        Test _slug_assert with illegal slug "¤"
        """
        slug = "¤"
        with self.assertRaises(AssertionError):
            self.tnp._slug_assert(slug)
 
    def test_str_multiple_words(self):
        """
        Test _slug_assert with illegal slug "goat horn"
        """
        slug = "goat horn"
        with self.assertRaises(AssertionError):
            self.tnp._slug_assert(slug)

if __name__ == "__main__":
    unittest.main()
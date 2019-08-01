import unittest

import context 

from TheNounProjectAPI.api import API
from TheNounProjectAPI.exceptions import IllegalSlug

class SlugAssert(unittest.TestCase):

    def setUp(self):
        key = "mock api key to satisfy type check in api._get_oauth()"
        secret = "mock secret key to satisfy type check in api._get_oauth()"
        self.api = API(key, secret, testing=True)

    def test_str(self):
        """
        Test _slug_assert with slug "goat"
        """
        slug = "goat"
        self.api._slug_assert(slug, "slug")
    
    def test_str_empty(self):
        """
        Test _slug_assert with illegal slug ""
        """
        slug = ""
        with self.assertRaises(IllegalSlug):
            self.api._slug_assert(slug, "slug")
 
    def test_str_non_ascii(self):
        """
        Test _slug_assert with illegal slug "¤"
        """
        slug = "¤"
        with self.assertRaises(IllegalSlug):
            self.api._slug_assert(slug, "slug")
 
    def test_str_multiple_words(self):
        """
        Test _slug_assert with illegal slug "goat horn"
        """
        slug = "goat horn"
        with self.assertRaises(IllegalSlug):
            self.api._slug_assert(slug, "slug")

if __name__ == "__main__":
    unittest.main()
import unittest

import context 

from src.api import API
from src.exceptions import IncorrectType

class UserCollectionURLs(unittest.TestCase):

    def setUp(self):
        key = "mock api key to satisfy type check in tnp._get_oauth()"
        secret = "mock secret key to satisfy type check in tnp._get_oauth()"
        self.tnp = API(key, secret, testing=True)

    def _test_get_user_collection(self, user_id, slug):
        """
        Helper function to call tnp's get_user_collection in such a way that we only get the URL
        and don't actually make the request.
        """
        return self.tnp.get_user_collection(user_id, slug).url

    def test_get_user_collection_legal(self):
        """
        Test URL for get_user_collection with user_id 12 and slug "goat"
        """
        expected = "http://api.thenounproject.com/user/12/collections/goat"
        user_id = 12
        slug = "goat"
        result = self._test_get_user_collection(user_id, slug)
        self.assertEqual(expected, result)

    def test_get_user_collection_illegal_id(self):
        """
        Test URL for get_user_collection with user_id None and slug "goat"
        """
        user_id = None
        slug = "goat"
        with self.assertRaises(IncorrectType):
            self._test_get_user_collection(user_id, slug)

    def test_get_user_collection_illegal_slug(self):
        """
        Test URL for get_user_collection with user_id 12 and slug None
        """
        user_id = 12
        slug = None
        with self.assertRaises(IncorrectType):
            self._test_get_user_collection(user_id, slug)

    def test_get_user_collection_illegal_id_illegal_slug(self):
        """
        Test URL for get_user_collection with user_id None and slug None
        """
        user_id = None
        slug = None
        with self.assertRaises(IncorrectType):
            self._test_get_user_collection(user_id, slug)

if __name__ == "__main__":
    unittest.main()
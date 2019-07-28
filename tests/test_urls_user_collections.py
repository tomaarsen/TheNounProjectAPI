import unittest

import context 
import src
from src import core
from src.core import TheNounProject

class UserCollectionsURLs(unittest.TestCase):

    def setUp(self):
        key = "mock api key to satisfy type check in tnp._get_oauth()"
        secret = "mock secret key to satisfy type check in tnp._get_oauth()"
        self.tnp = TheNounProject(key, secret, testing=True)

    def _test_get_user_collections(self, user_id):
        """
        Helper function to call tnp's get_user_collections in such a way that we only get the URL
        and don't actually make the request.
        """
        return self.tnp.get_user_collections(user_id).url

    def test_get_user_collections_legal(self):
        """
        Test URL for get_user_collections with user_id 12
        """
        expected = "http://api.thenounproject.com/user/12/collections"
        user_id = 12
        result = self._test_get_user_collections(user_id)
        self.assertEqual(expected, result)

    def test_get_user_collections_illegal_id(self):
        """
        Test URL for get_user_collections with user_id None
        """
        user_id = None
        with self.assertRaises(AssertionError):
            self._test_get_user_collections(user_id)

if __name__ == "__main__":
    unittest.main()
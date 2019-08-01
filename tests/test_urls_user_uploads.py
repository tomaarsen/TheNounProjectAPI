import unittest

import context 

from TheNounProjectAPI.api import API
from TheNounProjectAPI.exceptions import IncorrectType, IllegalTerm

class UserUploadsURLs(unittest.TestCase):

    def setUp(self):
        key = "mock api key to satisfy type check in api._get_oauth()"
        secret = "mock secret key to satisfy type check in api._get_oauth()"
        self.api = API(key, secret, testing=True)

    def _test_get_user_uploads(self, username):
        """
        Helper function to call api's get_user_uploads in such a way that we only get the URL
        and don't actually make the request.
        """
        return self.api.get_user_uploads(username).url

    def test_get_user_uploads_legal(self):
        """
        Test URL for get_user_uploads with username "goat"
        """
        expected = "http://api.thenounproject.com/user/goat/uploads"
        username = "goat"
        result = self._test_get_user_uploads(username)
        self.assertEqual(expected, result)

    def test_get_user_uploads_illegal_user_none(self):
        """
        Test URL for get_user_uploads with username None
        """
        username = None
        with self.assertRaises(IncorrectType):
            self._test_get_user_uploads(username)

    def test_get_user_uploads_illegal_user_empty(self):
        """
        Test URL for get_user_uploads with username ""
        """
        username = ""
        with self.assertRaises(IllegalTerm):
            self._test_get_user_uploads(username)

if __name__ == "__main__":
    unittest.main()
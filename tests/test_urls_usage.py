import unittest

import context 
import src
from src import core
from src.core import TheNounProject

class GetUsageURLs(unittest.TestCase):

    def setUp(self):
        key = "mock api key to satisfy type check in tnp._get_oauth()"
        secret = "mock secret key to satisfy type check in tnp._get_oauth()"
        self.tnp = TheNounProject(key, secret, testing=True)

    def _test_get_usage(self):
        """
        Helper function to call tnp's get_usage in such a way that we only get the URL
        and don't actually make the request.
        """
        return self.tnp.get_usage().url

    def test_get_usage(self):
        """
        Test URL for get_usage
        """
        expected = "http://api.thenounproject.com/oauth/usage"
        result = self._test_get_usage()
        self.assertEqual(expected, result)

if __name__ == "__main__":
    unittest.main()
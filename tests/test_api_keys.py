import unittest

import context 

from src.api import API
from src.exceptions import APIKeyNotSet

class ApiKeys(unittest.TestCase):

    def setUp(self):
        self.tnp = API(testing=True)
        self.key = "mock api key to satisfy type check in tnp._get_oauth()"
        self.secret = "mock secret key to satisfy type check in tnp._get_oauth()"

    def test_no_api_key_no_secret(self):
        """
        Attempt a request with no api key and no secret key
        """
        with self.assertRaises(APIKeyNotSet):
            self.tnp.get_usage()

    def test_no_api_key(self):
        """
        Attempt a request with no api key
        """
        self.tnp.set_secret_key(self.secret)
        with self.assertRaises(APIKeyNotSet):
            self.tnp.get_usage()
    
    def test_no_secret(self):
        """
        Attempt a request with no secret key
        """
        self.tnp.set_api_key(self.key)
        with self.assertRaises(APIKeyNotSet):
            self.tnp.get_usage()
    
    def test_both(self):
        """
        Attempt a request with both api and secret keys set
        """
        self.tnp.set_secret_key(self.secret)
        self.tnp.set_api_key(self.key)
        self.tnp.get_usage()

if __name__ == "__main__":
    unittest.main()
import unittest

import context 

from src.api import API
from src.exceptions import IncorrectType

class CollectionCustomURLs(unittest.TestCase):

    def setUp(self):
        key = "mock api key to satisfy type check in tnp._get_oauth()"
        secret = "mock secret key to satisfy type check in tnp._get_oauth()"
        self.tnp = API(key, secret, testing=True)

    def _test_get_collection(self, identifier):
        """
        Helper function to call tnp's get_collection in such a way that we only get the URL
        and don't actually make the request.
        """
        return self.tnp.get_collection(identifier).url

    def test_get_collection_int(self):
        """
        Test URL for get_collection with identifier 12
        """
        identifier = 12
        expected = "http://api.thenounproject.com/collection/12"
        result = self._test_get_collection(identifier)
        self.assertEqual(expected, result)

    def test_get_collection_str(self):
        """
        Test URL for get_collection with identifier "goat"
        """
        identifier = "goat"
        expected = "http://api.thenounproject.com/collection/goat"
        result = self._test_get_collection(identifier)
        self.assertEqual(expected, result)
    
    def test_get_collection_none(self):
        """
        Test URL for get_collection with illegal identifier None
        """
        identifier = None
        with self.assertRaises(IncorrectType):
            self._test_get_collection(identifier)

    def test_get_collection_bytes(self):
        """
        Test URL for get_collection with identifier b"goat"
        """
        identifier = b"goat"
        with self.assertRaises(IncorrectType):
            self._test_get_collection(identifier)

if __name__ == "__main__":
    unittest.main()
import unittest

import context 

from src.api import API
from src.exceptions import IncorrectType

class IconCustomURLs(unittest.TestCase):

    def setUp(self):
        key = "mock api key to satisfy type check in tnp._get_oauth()"
        secret = "mock secret key to satisfy type check in tnp._get_oauth()"
        self.tnp = API(key, secret, testing=True)

    def _test_get_icon(self, identifier):
        """
        Helper function to call tnp's get_icon in such a way that we only get the URL
        and don't actually make the request.
        """
        return self.tnp.get_icon(identifier).url

    def test_get_icon_legal_12(self):
        """
        Test URL for get_icon with id 12
        """
        identifier = 12
        expected = "http://api.thenounproject.com/icon/12"
        result = self._test_get_icon(identifier)
        self.assertEqual(expected, result)

    def test_get_icon_legal_goat(self):
        """
        Test URL for get_icon with identifier "goat"
        """
        identifier = "goat"
        expected = "http://api.thenounproject.com/icon/goat"
        result = self._test_get_icon(identifier)
        self.assertEqual(expected, result)

    def test_get_icon_illegal_identifier_float(self):
        """
        Test URL for get_icon with id 12.0
        """
        identifier = 12.0
        with self.assertRaises(IncorrectType):
            self._test_get_icon(identifier)

    def test_get_icon_illegal_identifier_none(self):
        """
        Test URL for get_icon with id None
        """
        identifier = None
        with self.assertRaises(IncorrectType):
            self._test_get_icon(identifier)

if __name__ == "__main__":
    unittest.main()
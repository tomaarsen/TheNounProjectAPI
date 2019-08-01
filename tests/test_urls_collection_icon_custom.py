import unittest

import context 

from TheNounProjectAPI.api import API
from TheNounProjectAPI.exceptions import IncorrectType

class CollectionIconsCustomURLs(unittest.TestCase):

    def setUp(self):
        key = "mock api key to satisfy type check in api._get_oauth()"
        secret = "mock secret key to satisfy type check in api._get_oauth()"
        self.api = API(key, secret, testing=True)

    def _test_get_collection_icons(self, identifier, limit=None, offset=None, page=None):
        """
        Helper function to call api's get_collection_icons in such a way that we only get the URL
        and don't actually make the request.
        """
        return self.api.get_collection_icons(identifier, limit=limit, offset=offset, page=page).url

    def test_get_collection_icons_legal_int(self):
        """
        Test URL for get_collection_icons with identifier 12
        """
        identifier = 12
        expected = "http://api.thenounproject.com/collection/12/icons"
        result = self._test_get_collection_icons(identifier)
        self.assertEqual(expected, result)

    def test_get_collection_icons_legal_string(self):
        """
        Test URL for get_collection_icons with identifier "goat"
        """
        identifier = "goat"
        expected = "http://api.thenounproject.com/collection/goat/icons"
        result = self._test_get_collection_icons(identifier)
        self.assertEqual(expected, result)

    def test_get_collection_icons_limit_page(self):
        """
        Test URL for get_collection_icons with identifier 12, with limit 12 and page 3
        """
        identifier = 12
        expected = "http://api.thenounproject.com/collection/12/icons?limit=12&page=3"
        limit = 12
        page = 3
        result = self._test_get_collection_icons(identifier, limit=limit, page=page)
        self.assertEqual(expected, result)

    def test_get_collection_icons_offset(self):
        """
        Test URL for get_collection_icons with identifier 12, with offset 12
        """
        identifier = 12
        expected = "http://api.thenounproject.com/collection/12/icons?offset=12"
        offset = 12
        result = self._test_get_collection_icons(identifier, offset=offset)
        self.assertEqual(expected, result)

    def test_get_collection_icons_illegal_identifier_none(self):
        """
        Test URL for get_collection_icons with ilegal identifier None
        """
        identifier = None
        with self.assertRaises(IncorrectType):
            self._test_get_collection_icons(identifier)

    def test_get_collection_icons_illegal_identifier_float(self):
        """
        Test URL for get_collection_icons with illegal identifier 12.0
        """
        identifier = 12.0
        with self.assertRaises(IncorrectType):
            self._test_get_collection_icons(identifier)

    def test_get_collection_icons_illegal_identifier_limit_page(self):
        """
        Test URL for get_collection_icons with illegal identifier [12, 4, 5], with legal limit 12 and page 3
        """
        identifier = [12, 4, 5]
        limit = 12
        page = 3
        with self.assertRaises(IncorrectType):
            self._test_get_collection_icons(identifier, limit=limit, page=page)

if __name__ == "__main__":
    unittest.main()
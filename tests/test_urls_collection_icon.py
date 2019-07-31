import unittest

import context 

from src.api import API
from src.exceptions import IncorrectType

class CollectionIconsURLs(unittest.TestCase):

    def setUp(self):
        key = "mock api key to satisfy type check in api._get_oauth()"
        secret = "mock secret key to satisfy type check in api._get_oauth()"
        self.api = API(key, secret, testing=True)

    def _test_get_collection_icons_by_id(self, _id, limit=None, offset=None, page=None):
        """
        Helper function to call api's get_collection_icons_by_id in such a way that we only get the URL
        and don't actually make the request.
        """
        return self.api.get_collection_icons_by_id(_id, limit=limit, offset=offset, page=page).url

    def test_get_collection_icons_by_id_legal(self):
        """
        Test URL for get_collection_icons with id 12
        """
        _id = 12
        expected = "http://api.thenounproject.com/collection/12/icons"
        result = self._test_get_collection_icons_by_id(_id)
        self.assertEqual(expected, result)

    def test_get_collection_icons_by_id_limit_page(self):
        """
        Test URL for get_collection_icons with id 12, with limit 12 and page 3
        """
        _id = 12
        expected = "http://api.thenounproject.com/collection/12/icons?limit=12&page=3"
        limit = 12
        page = 3
        result = self._test_get_collection_icons_by_id(_id, limit=limit, page=page)
        self.assertEqual(expected, result)

    def test_get_collection_icons_by_id_offset(self):
        """
        Test URL for get_collection_icons with id 12, with offset 12
        """
        _id = 12
        expected = "http://api.thenounproject.com/collection/12/icons?offset=12"
        offset = 12
        result = self._test_get_collection_icons_by_id(_id, offset=offset)
        self.assertEqual(expected, result)

    def test_get_collection_icons_by_id_illegal_identifier(self):
        """
        Test URL for get_collection_icons with illegal id 12.0
        """
        _id = 12.0
        with self.assertRaises(IncorrectType):
            self._test_get_collection_icons_by_id(_id)





    def _test_get_collection_icons_by_slug(self, slug, limit=None, offset=None, page=None):
        """
        Helper function to call api's get_collection_icons_by_slug in such a way that we only get the URL
        and don't actually make the request.
        """
        return self.api.get_collection_icons_by_slug(slug, limit=limit, offset=offset, page=page).url

    def test_get_collection_icons_by_slug_legal(self):
        """
        Test URL for get_collection_icons with slug "goat"
        """
        slug = "goat"
        expected = "http://api.thenounproject.com/collection/goat/icons"
        result = self._test_get_collection_icons_by_slug(slug)
        self.assertEqual(expected, result)

    def test_get_collection_icons_by_slug_limit_page(self):
        """
        Test URL for get_collection_icons with slug "goat", with limit 12 and page 3
        """
        slug = "goat"
        expected = "http://api.thenounproject.com/collection/goat/icons?limit=12&page=3"
        limit = 12
        page = 3
        result = self._test_get_collection_icons_by_slug(slug, limit=limit, page=page)
        self.assertEqual(expected, result)

    def test_get_collection_icons_by_slug_offset(self):
        """
        Test URL for get_collection_icons with slug "goat", with offset 12
        """
        slug = "goat"
        expected = "http://api.thenounproject.com/collection/goat/icons?offset=12"
        offset = 12
        result = self._test_get_collection_icons_by_slug(slug, offset=offset)
        self.assertEqual(expected, result)

    def test_get_collection_icons_by_slug_illegal_identifier(self):
        """
        Test URL for get_collection_icons with illegal slug 12
        """
        slug = 12
        with self.assertRaises(IncorrectType):
            self._test_get_collection_icons_by_slug(slug)

if __name__ == "__main__":
    unittest.main()
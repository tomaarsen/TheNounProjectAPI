import unittest

import context 

from TheNounProjectAPI.api import API
from TheNounProjectAPI.exceptions import IncorrectType

class CollectionURLs(unittest.TestCase):

    def setUp(self):
        key = "mock api key to satisfy type check in api._get_oauth()"
        secret = "mock secret key to satisfy type check in api._get_oauth()"
        self.api = API(key, secret, testing=True)

    def _test_get_collection_by_id(self, _id):
        """
        Helper function to call api's get_collection_by_id in such a way that we only get the URL
        and don't actually make the request.
        """
        return self.api.get_collection_by_id(_id).url

    def test_get_collection_by_id_legal_12(self):
        """
        Test URL for get_collection_by_id with id 12
        """
        _id = 12
        expected = "http://api.thenounproject.com/collection/12"
        result = self._test_get_collection_by_id(_id)
        self.assertEqual(expected, result)

    def test_get_collection_by_id_illegal_id_float(self):
        """
        Test URL for get_collection_by_id with id 12.0
        """
        _id = 12.0
        with self.assertRaises(IncorrectType):
            self._test_get_collection_by_id(_id)

    def test_get_collection_by_id_illegal_id_none(self):
        """
        Test URL for get_collection_by_id with id None
        """
        _id = None
        with self.assertRaises(IncorrectType):
            self._test_get_collection_by_id(_id)




    def _test_get_collection_by_slug(self, slug):
        """
        Helper function to call api's get_collection_by_slug in such a way that we only get the URL
        and don't actually make the request.
        """
        return self.api.get_collection_by_slug(slug).url

    def test_get_collection_by_slug_legal_goat(self):
        """
        Test URL for get_collection_by_slug with slug "goat"
        """
        slug = "goat"
        expected = "http://api.thenounproject.com/collection/goat"
        result = self._test_get_collection_by_slug(slug)
        self.assertEqual(expected, result)

    def test_get_collection_by_slug_illegal_slug_float(self):
        """
        Test URL for get_collection_by_slug with slug 12.0
        """
        slug = 12.0
        with self.assertRaises(IncorrectType):
            self._test_get_collection_by_slug(slug)

    def test_get_collection_by_slug_illegal_slug_none(self):
        """
        Test URL for get_collection_by_slug with slug None
        """
        slug = None
        with self.assertRaises(IncorrectType):
            self._test_get_collection_by_slug(slug)

if __name__ == "__main__":
    unittest.main()
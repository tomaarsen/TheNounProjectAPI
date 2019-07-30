import unittest

import context 


from src.api import API

class IconURLs(unittest.TestCase):

    def setUp(self):
        key = "mock api key to satisfy type check in tnp._get_oauth()"
        secret = "mock secret key to satisfy type check in tnp._get_oauth()"
        self.tnp = API(key, secret, testing=True)

    def _test_get_icon_by_id(self, _id):
        """
        Helper function to call tnp's get_icon_by_id in such a way that we only get the URL
        and don't actually make the request.
        """
        return self.tnp.get_icon_by_id(_id).url

    def test_get_icon_by_id_legal_12(self):
        """
        Test URL for get_icon_by_id with id 12
        """
        _id = 12
        expected = "http://api.thenounproject.com/icon/12"
        result = self._test_get_icon_by_id(_id)
        self.assertEqual(expected, result)

    def test_get_icon_by_id_illegal_id_float(self):
        """
        Test URL for get_icon_by_id with id 12.0
        """
        _id = 12.0
        with self.assertRaises(AssertionError):
            self._test_get_icon_by_id(_id)

    def test_get_icon_by_id_illegal_id_none(self):
        """
        Test URL for get_icon_by_id with id None
        """
        _id = None
        with self.assertRaises(AssertionError):
            self._test_get_icon_by_id(_id)




    def _test_get_icon_by_term(self, term):
        """
        Helper function to call tnp's get_icon_by_term in such a way that we only get the URL
        and don't actually make the request.
        """
        return self.tnp.get_icon_by_term(term).url

    def test_get_icon_by_term_legal_goat(self):
        """
        Test URL for get_icon_by_term with term "goat"
        """
        term = "goat"
        expected = "http://api.thenounproject.com/icon/goat"
        result = self._test_get_icon_by_term(term)
        self.assertEqual(expected, result)

    def test_get_icon_by_term_illegal_term_float(self):
        """
        Test URL for get_icon_by_term with term 12.0
        """
        term = 12.0
        with self.assertRaises(AssertionError):
            self._test_get_icon_by_term(term)

    def test_get_icon_by_term_illegal_term_none(self):
        """
        Test URL for get_icon_by_term with term None
        """
        term = None
        with self.assertRaises(AssertionError):
            self._test_get_icon_by_term(term)

if __name__ == "__main__":
    unittest.main()
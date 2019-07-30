import unittest

import context 


from src.api import API

class IconsURLs(unittest.TestCase):

    def setUp(self):
        key = "mock api key to satisfy type check in tnp._get_oauth()"
        secret = "mock secret key to satisfy type check in tnp._get_oauth()"
        self.tnp = API(key, secret, testing=True)

    def _test_get_icons_by_term(self, term, public_domain_only=False, limit=None, offset=None, page=None):
        """
        Helper function to call tnp's get_icons_by_term in such a way that we only get the URL
        and don't actually make the request.
        """
        return self.tnp.get_icons_by_term(term, public_domain_only, limit, offset, page).url

    def test_get_icons_by_term_legal_goat(self):
        """
        Test URL for get_icons_by_term with term "goat"
        """
        term = "goat"
        expected = "http://api.thenounproject.com/icons/goat?limit_to_public_domain=0"
        result = self._test_get_icons_by_term(term)
        self.assertEqual(expected, result)

    def test_get_icons_by_term_illegal_term_float(self):
        """
        Test URL for get_icons_by_term with term 12.0
        """
        term = 12.0
        with self.assertRaises(AssertionError):
            self._test_get_icons_by_term(term)

    def test_get_icons_by_term_illegal_term_none(self):
        """
        Test URL for get_icons_by_term with term None
        """
        term = None
        with self.assertRaises(AssertionError):
            self._test_get_icons_by_term(term)

    def test_get_icons_by_term_public_domain_true(self):
        """
        Test URL for get_icons_by_term with term "goat", with public_domain_only as True
        """
        term = "goat"
        public_domain_only = True
        expected = "http://api.thenounproject.com/icons/goat?limit_to_public_domain=1"
        result = self._test_get_icons_by_term(term, public_domain_only=public_domain_only)
        self.assertEqual(expected, result)

    def test_get_icons_by_term_public_domain_false(self):
        """
        Test URL for get_icons_by_term with term "goat", with public_domain_only as False
        """
        term = "goat"
        public_domain_only = False
        expected = "http://api.thenounproject.com/icons/goat?limit_to_public_domain=0"
        result = self._test_get_icons_by_term(term, public_domain_only=public_domain_only)
        self.assertEqual(expected, result)

    def test_get_icons_by_term_public_domain_int(self):
        """
        Test URL for get_icons_by_term with term "goat", with public_domain_only as 12
        Note that I'll allow any integer value, even zero and negative numbers.
        """
        term = "goat"
        public_domain_only = 12
        expected = "http://api.thenounproject.com/icons/goat?limit_to_public_domain=12"
        result = self._test_get_icons_by_term(term, public_domain_only=public_domain_only)
        self.assertEqual(expected, result)

    def test_get_icons_by_term_public_domain_illegal(self):
        """
        Test URL for get_icons_by_term with term "goat", with public_domain_only as "goat"
        """
        term = "goat"
        public_domain_only = "goat"
        with self.assertRaises(AssertionError):
            self._test_get_icons_by_term(term, public_domain_only=public_domain_only)

if __name__ == "__main__":
    unittest.main()
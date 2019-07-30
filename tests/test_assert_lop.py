import unittest

import context 


from src.api import API

class SlugAssert(unittest.TestCase):

    def setUp(self):
        key = "mock api key to satisfy type check in tnp._get_oauth()"
        secret = "mock secret key to satisfy type check in tnp._get_oauth()"
        self.tnp = API(key, secret, testing=True)

    def _test_lop(self, limit=None, offset=None, page=None):
        """
        Helper method to call tnp's _lop_assert
        """
        self.tnp._lop_assert(limit, offset, page)

    def test_lop_limit_none(self):
        """
        Test to see that limit as None does not throw an exception
        """
        limit = None
        self._test_lop(limit=limit)

    def test_lop_limit_int(self):
        """
        Test to see that limit as 12 does not throw an exception
        """
        limit = 12
        self._test_lop(limit=limit)

    def test_lop_limit_illegal(self):
        """
        Test to see that limit as "goat" throws an exception
        """
        limit = "goat"
        with self.assertRaises(AssertionError):
            self._test_lop(limit=limit)

    def test_lop_offset_none(self):
        """
        Test to see that offset as None does not throw an exception
        """
        offset = None
        self._test_lop(offset=offset)

    def test_lop_offset_int(self):
        """
        Test to see that offset as 12 does not throw an exception
        """
        offset = 12
        self._test_lop(offset=offset)

    def test_lop_offset_illegal(self):
        """
        Test to see that offset as "goat" throws an exception
        """
        offset = "goat"
        with self.assertRaises(AssertionError):
            self._test_lop(offset=offset)

    def test_lop_page_none(self):
        """
        Test to see that page as None does not throw an exception
        """
        page = None
        self._test_lop(page=page)

    def test_lop_page_int(self):
        """
        Test to see that page as 12 does not throw an exception
        """
        page = 12
        self._test_lop(page=page)

    def test_lop_page_illegal(self):
        """
        Test to see that page as "goat" throws an exception
        """
        page = "goat"
        with self.assertRaises(AssertionError):
            self._test_lop(page=page)

if __name__ == "__main__":
    unittest.main()
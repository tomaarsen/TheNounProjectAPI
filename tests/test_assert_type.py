import unittest

import context 

from src.api import API
from src.exceptions import IncorrectType

class SlugAssert(unittest.TestCase):

    def setUp(self):
        key = "mock api key to satisfy type check in tnp._get_oauth()"
        secret = "mock secret key to satisfy type check in tnp._get_oauth()"
        self.tnp = API(key, secret, testing=True)

    def _test_type(self, param, param_name, types):
        """
        Helper method to call tnp's _type_assert
        """
        self.tnp._type_assert(param, param_name, types)

    def test_type_legal_none(self):
        """
        Test to see that param as None with type(None) in types does not throw an exception
        """
        goat = None
        param_name = "goat"
        types = (type(None), int, str)
        self._test_type(goat, param_name, types)

    def test_type_legal_str(self):
        """
        Test to see that param as str with str in types does not throw an exception
        """
        goat = "goat"
        param_name = "goat"
        types = (type(None), int, str)
        self._test_type(goat, param_name, types)

    def test_type_legal_int(self):
        """
        Test to see that param as int with int in types does not throw an exception
        """
        goat = 12
        param_name = "goat"
        types = int
        self._test_type(goat, param_name, types)

    def test_type_illegal_none(self):
        """
        Test to see that param as None with type(None) not in types throws an exception
        """
        goat = None
        param_name = "goat"
        types = (tuple, int, str)
        with self.assertRaises(IncorrectType):
            self._test_type(goat, param_name, types)

    def test_type_illegal_float(self):
        """
        Test to see that param as float with float not in types throws an exception
        """
        goat = 12.0
        param_name = "goat"
        types = (int, str)
        with self.assertRaises(IncorrectType):
            self._test_type(goat, param_name, types)

    def test_type_illegal_bytes(self):
        """
        Test to see that param as bytes with bytes not in types throws an exception
        """
        goat = b"goat"
        param_name = "goat"
        types = str
        with self.assertRaises(IncorrectType):
            self._test_type(goat, param_name, types)

if __name__ == "__main__":
    unittest.main()
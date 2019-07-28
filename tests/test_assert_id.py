import unittest

import context 
import src
from src import wrapper
from src.wrapper import TheNounProject

class IdAssert(unittest.TestCase):

    def setUp(self):
        key = "mock api key to satisfy type check in tnp._get_oauth()"
        secret = "mock secret key to satisfy type check in tnp._get_oauth()"
        self.tnp = TheNounProject(key, secret, testing=True)

    def test_id_12(self):
        """
        Test _id_assert with id 12
        """
        id = 12
        self.tnp._id_assert(id)
    
    def test_id_neg_12(self):
        """
        Test _id_assert with illegal id -12
        """
        id = -12
        with self.assertRaises(AssertionError):
            self.tnp._id_assert(id)
 
    def test_id_0(self):
        """
        Test _id_assert with illegal id 0
        """
        id = 0
        with self.assertRaises(AssertionError):
            self.tnp._id_assert(id)

if __name__ == "__main__":
    unittest.main()
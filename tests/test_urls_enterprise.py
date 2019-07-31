import unittest

import context
import json

from src.api import API
from src.exceptions import IncorrectType

class SlugAssert(unittest.TestCase):

    def setUp(self):
        key = "mock api key to satisfy type check in tnp._get_oauth()"
        secret = "mock secret key to satisfy type check in tnp._get_oauth()"
        self.tnp = API(key, secret, testing=True)

    def _test_report_usage(self, icons, test=False):
        """
        Helper method to call tnp's report_usage
        """
        return self.tnp.report_usage(icons, test)

    def _check_set(self, body, input_set):
        """
        Helper method for comparing PreparedRequest body with a set of icon ids.
        """
        json_data = json.loads(body.decode())
        icons_str = json_data['icons']
        icons_set = set(icons_str.split(","))
        return icons_set == {str(item) for item in input_set}

    def test_report_usage_int(self):
        """
        Test URL and body for report_usage, with icons as 12
        """
        icons = 12
        expected_url = "http://api.thenounproject.com/notify/publish"
        expected_body = b'{"icons": "12"}'
        result = self._test_report_usage(icons)
        self.assertEqual(result.url, expected_url)
        self.assertEqual(result.body, expected_body)

    def test_report_usage_str(self):
        """
        Test URL and body for report_usage, with icons as "12"
        """
        icons = "12"
        expected_url = "http://api.thenounproject.com/notify/publish"
        expected_body = b'{"icons": "12"}'
        result = self._test_report_usage(icons)
        self.assertEqual(result.url, expected_url)
        self.assertEqual(result.body, expected_body)

    def test_report_usage_set(self):
        """
        Test URL and body for report_usage, with icons as {12, "4", 8, 12}
        """
        icons = {12, "4", 8, 12}
        expected_url = "http://api.thenounproject.com/notify/publish"
        result = self._test_report_usage(icons)
        self.assertEqual(result.url, expected_url)
        self.assertTrue(self._check_set(result.body, icons))

    def test_report_usage_list(self):
        """
        Test URL and body for report_usage, with icons as ["4", 8, 12]
        """
        icons = ["4", 8, 12]
        expected_url = "http://api.thenounproject.com/notify/publish"
        expected_body = b'{"icons": "4,8,12"}'
        result = self._test_report_usage(icons)
        self.assertEqual(result.url, expected_url)
        self.assertEqual(result.body, expected_body)

    def test_report_usage_none(self):
        """
        Test URL and body for report_usage, with icons as None
        """
        icons = None
        with self.assertRaises(IncorrectType):
            self._test_report_usage(icons)

    def test_report_usage_float(self):
        """
        Test URL and body for report_usage, with icons as 12.0
        """
        icons = 12.0
        with self.assertRaises(IncorrectType):
            self._test_report_usage(icons)

    def test_report_usage_int_test(self):
        """
        Test URL and body for report_usage, with icons as "12", and test as True
        """
        icons = "12"
        expected_url = "http://api.thenounproject.com/notify/publish?test=1"
        expected_body = b'{"icons": "12"}'
        result = self._test_report_usage(icons, test=True)
        self.assertEqual(result.url, expected_url)
        self.assertEqual(result.body, expected_body)

    def test_report_usage_set_test(self):
        """
        Test URL and body for report_usage, with icons as {12, "4", 8, 12}, and test as True
        """
        icons = {12, "4", 8, 12}
        expected_url = "http://api.thenounproject.com/notify/publish?test=1"
        result = self._test_report_usage(icons, test=True)
        self.assertEqual(result.url, expected_url)
        self.assertTrue(self._check_set(result.body, icons))

if __name__ == "__main__":
    unittest.main()
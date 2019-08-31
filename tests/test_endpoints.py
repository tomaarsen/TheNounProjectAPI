import unittest, os

import context 

from TheNounProjectAPI.api import API
from TheNounProjectAPI.models import CollectionModel
from TheNounProjectAPI.exceptions import NotFound

class Endpoints(unittest.TestCase):

    def setUp(self):
        try:
            key = os.environ["TNP_KEY"]
            secret = os.environ["TNP_SECRET"]
        except KeyError:
            raise unittest.SkipTest("We skip tests sending actual requests if the key and secret are not set as environment variables.")
        self.api = API(key, secret)
        self.limit = 2
        self.common_attributes = {"permalink", "id", "sponsor", "sponsor_id", "sponsor_campaign_link"}
        self.usage_attributes = {"limits", "usage"}
        self.usage_time_attributes = {"daily", "hourly", "monthly"}
        self.report_usage_attributes = {"licenses_consumed", "result"}

    def tearDown(self):
        self.api._close_session()

    def test_collection_by_id(self):
        """
        Check if the result has self.common_attributes as attributes.
        """
        result = self.api.get_collection(12)
        self.assertTrue(self.common_attributes <= set(result.json.keys()))

    def test_collection_by_slug(self):
        """
        Check if the result has self.common_attributes as attributes.
        """
        result = self.api.get_collection("cue")
        self.assertTrue(self.common_attributes <= set(result.json.keys()))

    def test_collections(self):
        """
        Check if the result has a list of objects with self.common_attributes as attributes.
        """
        result = self.api.get_collections(limit=self.limit)
        for collection in result:
            self.assertTrue(self.common_attributes <= set(collection.json.keys()))

    def test_user_collections(self):
        """
        Check if the result has a list of objects with self.common_attributes as attributes.
        """
        result = self.api.get_user_collections(6)
        for collection in result:
            self.assertTrue(self.common_attributes <= set(collection.json.keys()))

    def test_user_collection(self):
        result = self.api.get_user_collection(6, "truck")
        self.assertTrue(self.common_attributes <= set(result.json.keys()))

    def test_report_usage(self):
        """
        Check if the result has self.report_usage_attributes as attributes.
        """
        result = self.api.report_usage([3, 8, 12], test=True)
        self.assertTrue(self.report_usage_attributes <= set(result.json.keys()))

    def test_collection_icons_by_id(self):
        """
        Check if the result.collection has self.common_attributes as attributes.
        Also ensure that the each icon under result has self.common_attributes as attributes.
        Lastly check that result has generated_at as attribute.
        """
        result = self.api.get_collection_icons(12, limit=self.limit)
        self.assertTrue(hasattr(result, "generated_at"))
        self.assertTrue(self.common_attributes <= set(result.collection.keys()))
        for icon in result:
            self.assertTrue(self.common_attributes <= set(icon.json.keys()))

    def test_collection_icons_by_slug(self):
        """
        Check if the result.collection has self.common_attributes as attributes.
        Also ensure that the each icon under result has self.common_attributes as attributes.
        Lastly check that result has generated_at as attribute.
        """
        result = self.api.get_collection_icons("cue", limit=self.limit)
        self.assertTrue(hasattr(result, "generated_at"))
        self.assertTrue(self.common_attributes <= set(result.collection.keys()))
        for icon in result:
            self.assertTrue(self.common_attributes <= set(icon.json.keys()))

    def test_icon_by_id(self):
        """
        Check if the result has self.common_attributes as attributes.
        Also ensure that the result.collection list has self.common_attributes as attributes for all of its elements.
        """
        result = self.api.get_icon(12)
        self.assertTrue(self.common_attributes <= set(result.json.keys()))
        for collection in result.collections:
            self.assertTrue(self.common_attributes <= set(CollectionModel.parse(collection).json.keys()))

    def test_icon_by_term(self):
        """
        Check if the result has self.common_attributes as attributes.
        Also ensure that the result.collection list has self.common_attributes as attributes for all of its elements.
        """
        result = self.api.get_icon("baggage")
        self.assertTrue(self.common_attributes <= set(result.json.keys()))
        for collection in result.collections:
            self.assertTrue(self.common_attributes <= set(CollectionModel.parse(collection).json.keys()))

    def test_recent_icons(self):
        """
        Check if each icon under result has self.common_attributes as attributes.
        Also ensure that result has generated_at as attribute.
        """
        result = self.api.get_recent_icons(limit=self.limit)
        self.assertTrue(hasattr(result, "generated_at"))
        for icon in result:
            self.assertTrue(self.common_attributes <= set(icon.json.keys()))

    def test_icons_by_term(self):
        """
        Check if each icon under result has self.common_attributes as attributes.
        Also ensure that result has generated_at as attribute.
        """
        result = self.api.get_icons_by_term("goat", limit=self.limit)
        self.assertTrue(hasattr(result, "generated_at"))
        for icon in result:
            self.assertTrue(self.common_attributes <= set(icon.json.keys()))

    def test_user_uploads(self):
        """
        Check if each icon under result has self.common_attributes as attributes.
        Also ensure that result has generated_at as attribute.
        """
        result = self.api.get_user_uploads("dan", limit=self.limit)
        self.assertTrue(hasattr(result, "generated_at"))
        for icon in result:
            self.assertTrue(self.common_attributes <= set(icon.json.keys()))

    def test_usage(self):
        """
        Check if the result has self.usage_attributes as attributes.
        Also check if result.limits 
        """
        result = self.api.get_usage()
        self.assertTrue(set(result.json.keys()) == self.usage_attributes)
        self.assertTrue(set(result.json.limits.keys()) == self.usage_time_attributes)
        self.assertTrue(set(result.json.usage.keys()) == self.usage_time_attributes)

    def test_invalid_icon(self):
        """
        Check if getting an icon with an invalid id produces the correct NotFound exception.
        """
        invalid_id = int(1e15)
        with self.assertRaises(NotFound):
            self.api.get_icon(invalid_id)

if __name__ == "__main__":
    unittest.main() 
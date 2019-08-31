import unittest

import context 

from TheNounProjectAPI.models import Model, CollectionModel, CollectionsModel, UsageModel

class Models(unittest.TestCase):

    def setUp(self):
        data = {
                    "author": [{"location": "",
                                "name": "TukTuk Design",
                                "permalink": "/tuktukdesign",
                                "username": "tuktukdesign"}],
                    "author_id": "319644",
                    "date_created": "2014-06-15 13:59:41",
                    "date_updated": "2014-06-15 14:00:38",
                    "description": "",
                    "icon_count": "18",
                    "id": "220",
                    "is_collaborative": "",
                    "is_featured": "0",
                    "is_published": "1",
                    "is_store_item": "0",
                    "name": "Arrows-1",
                    "permalink": "/tuktukdesign/collection/arrows-1",
                    "slug": "arrows-1",
                    "sponsor": {},
                    "sponsor_campaign_link": "",
                    "sponsor_id": "",
                    "tags": ["arrow",
                            "arrows",
                            "up",
                            "down",
                            "left",
                            "right",
                            "up arrow",
                            "down arrow",
                            "left arrow",
                            "right arrow",
                            "up arrows",
                            "down arrows",
                            "left arrows",
                            "right arrows"],
                    "template": "24"
                }
        self.model = Model.parse(data)
        self.col_model = CollectionModel.parse(data)
        self.cols_model = CollectionsModel.parse( {"collections": [data, data, data]} )
        usage_data = {
                        "limits": {
                            "daily": None,
                            "hourly": None,
                            "monthly": 5000
                        },
                        "usage": {
                            "daily": 30,
                            "hourly": 16,
                            "monthly": 32
                        }
                    }
        self.usage_model = UsageModel.parse(usage_data)
    
    def test_get_attr(self):
        """
        Assure that model.json['data'] is always equivalent to model.data
        """
        self.assertTrue(all([getattr(self.model, name) == self.model.json[name] for name in self.model.json]))

    def test_get_item(self):
        """
        Assure that model.json['data'] is always equivalent to model['data']
        """
        self.assertTrue(all([self.model[name] == self.model.json[name] for name in self.model.json]))

    def test_collection_repr(self):
        """
        Assure that CollectionModel is printed properly.
        """
        self.assertEqual(str(self.col_model), "<CollectionModel: Name: Arrows-1, Slug: arrows-1, Id: 220>")

    def test_usage_repr(self):
        """
        Assure that UsageModel is printed properly.
        """
        self.assertEqual(str(self.usage_model), "<UsageModel: Hourly: 16, Daily: 30, Monthly: 32>")

    def test_collections_repr(self):
        """
        Assure that CollectionsModel is printed properly.
        """
        self.assertEqual(str(self.cols_model), "[<CollectionModel: Name: Arrows-1, Slug: arrows-1, Id: 220>, <CollectionModel: Name: Arrows-1, Slug: arrows-1, Id: 220>, <CollectionModel: Name: Arrows-1, Slug: arrows-1, Id: 220>]")

    def test_dot_list_to_dot_dict(self):
        """
        Assure that dot_dict[0][2].data is equivalent to dot_dict[0][2]['data']. 
        """
        self.assertEqual(self.model.author[0].username, "tuktukdesign")

    def test_dot_dict_attr_error(self):
        """
        Assure that DotDict throws an exception if dot_dict.value is used when value not in dot_dict.
        """
        with self.assertRaises(AttributeError):
            self.model.value

if __name__ == "__main__":
    unittest.main()
Example outputs
***************

.. _collection-label:

Collection
==========

:py:class:`~TheNounProjectAPI.models.CollectionModel` will return an instance, each with the following json structure:

.. code-block:: json

    {
        "author": {"location": "",
                    "name": "TukTuk Design",
                    "permalink": "/tuktukdesign",
                    "username": "tuktukdesign"},
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

.. note::
    How this data may be accessed after a request is described in :py:class:`~TheNounProjectAPI.models.Model`.

.. _collections-label:

Collections
===========

:py:class:`~TheNounProjectAPI.models.CollectionsModel` will return a list of :py:class:`~TheNounProjectAPI.models.CollectionModel` objects, each with the following json structure:

.. code-block:: json

    {
        "author": {"location": "Islamabad, Capital, PK",
                    "name": "Flatart",
                    "permalink": "/Flatart",
                    "username": "Flatart"},
        "author_id": "4478358",
        "date_created": "2019-08-02 10:55:16",
        "date_updated": "2019-08-02 10:55:16",
        "description": "",
        "id": "88003",
        "is_collaborative": "",
        "is_featured": "0",
        "is_published": "1",
        "is_store_item": "0",
        "name": "Maps & Travel",
        "permalink": "/Flatart/collection/maps-travel",
        "slug": "maps-travel",
        "sponsor": {},
        "sponsor_campaign_link": "",
        "sponsor_id": "",
        "tags": [],
        "template": "24"
    }

A method returning :py:class:`~TheNounProjectAPI.models.CollectionsModel` in reality returns a list with some additional attributes:

* `collections` holding a list of :py:class:`~TheNounProjectAPI.models.DotDict` objects, each with a collection.
* `response` holding a requests.Response object of the request.

Furthermore, each element in the list may be accessed like :py:class:`~TheNounProjectAPI.models.Model`.

.. _icon-label:

Icon
====

.. _icons-label:

Icons
=====

:py:class:`~TheNounProjectAPI.models.IconsModel` will return a list of :py:class:`~TheNounProjectAPI.models.IconModel` objects, each with the following json structure:

.. code-block:: json

    {
        "attribution": "Double Tap by P.J. Onori from Noun Project",
        "date_uploaded": "2012-05-21",
        "icon_url": "<manually truncated>",
        "id": "2913",
        "is_active": "1",
        "is_explicit": "0",
        "license_description": "public-domain",
        "nounji_free": "0",
        "permalink": "/term/double-tap/2913",
        "preview_url": "https://static.thenounproject.com/png/2913-200.png",
        "preview_url_42": "https://static.thenounproject.com/png/2913-42.png",
        "preview_url_84": "https://static.thenounproject.com/png/2913-84.png",
        "sponsor": {},
        "sponsor_campaign_link": null,
        "sponsor_id": "",
        "tags": [{"id": 4088, "slug": "double-tap"},
                {"id": 2028, "slug": "finger"},
                {"id": 2839, "slug": "interface"},
                {"id": 443, "slug": "ipad"},
                {"id": 440, "slug": "iphone"},
                {"id": 908, "slug": "mobile"},
                {"id": 1293, "slug": "screen"},
                {"id": 1393, "slug": "tablet"},
                {"id": 2816, "slug": "touch"}],
        "term": "Double Tap",
        "term_id": 4088,
        "term_slug": "double-tap",
        "updated_at": "2019-04-22 19:22:17",
        "uploader": {"location": "San Francisco, US",
                    "name": "P.J. Onori",
                    "permalink": "/somerandomdude",
                    "username": "somerandomdude"},
        "uploader_id": "5652",
        "year": 2009
    }

A method returning :py:class:`~TheNounProjectAPI.models.IconsModel` in reality returns a list with some additional attributes:

* `icons` holding a list of :py:class:`~TheNounProjectAPI.models.DotDict` objects, each with an icon.
* `collection` holding a :py:class:`~TheNounProjectAPI.models.DotDict` object, with the collection the icons come from.
* `generated_at` holding a string indicating when the request was generated.
* `response` holding a requests.Response object of the request.

Furthermore, each element in the list may be accessed like :py:class:`~TheNounProjectAPI.models.Model`.

.. warning::
    Some requests return slightly different values. For example, some collection icons have a `attribution_preview_url`, while some do not.
Models
------------------------------

.. automodule:: TheNounProjectAPI.models
    :members:
    :show-inheritance:
    :exclude-members: Model
    :member-order: bysource

    .. class:: Model
        
        Model is a base class to be used as a superclass for conveniently accessing data.
        All of the json returned by the API is parsed through this model, and stored under the :attr:`json` attribute.
        
        Let's assume the json looks like this:

        .. code-block:: json

            {
                "author": {
                    "location": "US",
                    "name": "mnmly",
                    "permalink": "/mnmly",
                    "username": "mnmly"
                },
                "author_id": "1",
                "date_created": "2012-02-22 13:32:49",
                "date_updated": "2012-02-22 13:33:00",
                "description": "",
                "icon_count": "3",
                "id": "7",
                "is_collaborative": "",
                "is_featured": "0",
                "is_published": "0",
                "is_store_item": "1",
                "name": "Bicycle",
                "permalink": "/mnmly/collection/bicycle",
                "slug": "bicycle",
                "sponsor": {},
                "sponsor_campaign_link": "",
                "sponsor_id": "",
                "tags": [],
                "template": "24"
            }
        

        This data may then be accessed in any of the following ways:

        .. code-block :: python

            # (A) Standard way for accessing a dict
            model.json["author"]["username"]

            # This standard way may also be applied directly to the model object.
            model["author"]["username"]

            # Dot notation may also be used, both on the json attribute, or on the model object.
            model.json.author.username
            model.author.username

        .. attribute:: json

            The json data returned by the API, as a :class:`DotDict` instance.

        .. attribute:: response

            The requests.Response object returned by sending the request.

        .. automethod:: parse

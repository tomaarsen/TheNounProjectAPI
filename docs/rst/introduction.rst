Introduction
=========================

<Introduction>

Getting Started
===============

API keys
^^^^^^^^

Before any requests can be made, the api key and secret need to be set.
These keys can be generated once you have made a Noun Project account. 
See `this topic <https://api.thenounproject.com/getting_started.html#creating-an-api-key>`_ on the official Noun Project documentation for more information.

Once you have generated these keys, they need to be set in the api wrapper. This can be done in a few ways. 
For each of these ways, assume that this section of code is present at the top:

.. code-block :: python
    :linenos:

    import TheNounProjectAPI
    key = "<sample api key>"
    secret = "<sample secret key>"

You can pass the keys to the constructor when creating the object:

.. code-block :: python
    :lineno-start: 4

    api = TheNounProjectAPI.API(key=key, secret=secret)

You can also set the attributes directly:

.. code-block :: python
    :lineno-start: 4

    api = TheNounProjectAPI.API()
    api.api_key = key
    api.secret_key = secret

Or call the api key and secret key setters:

.. code-block :: python
    :lineno-start: 4

    api = TheNounProjectAPI.API()
    api.set_api_key(key)
    api.set_secret_key(secret)

Making requests
^^^^^^^^^^^^^^^

Now that we have an API object with the keys set properly, we can start making requests. 
Let's take a look at some of the most useful methods:

========================================================== =======================
Methods                                                    Example output
========================================================== =======================
:py:meth:`~TheNounProjectAPI.api.API.get_collection`       :ref:`collection-label`
:py:meth:`~TheNounProjectAPI.api.API.get_collection_icons` :ref:`icons-label`
:py:meth:`~TheNounProjectAPI.api.API.get_collections`      :ref:`collections-label`
:py:meth:`~TheNounProjectAPI.api.API.get_icon`             :ref:`icon-label`
:py:meth:`~TheNounProjectAPI.api.API.get_icons_by_term`    :ref:`icons-label`
:py:meth:`~TheNounProjectAPI.api.API.get_recent_icons`     :ref:`icons-label`
:py:meth:`~TheNounProjectAPI.api.API.get_usage`            :ref:`usage-label`
:py:meth:`~TheNounProjectAPI.api.API.get_user_collection`  :ref:`collection-label`
:py:meth:`~TheNounProjectAPI.api.API.get_user_collections` :ref:`collections-label`
:py:meth:`~TheNounProjectAPI.api.API.get_user_uploads`     :ref:`icons-label`
:py:meth:`~TheNounProjectAPI.api.API.report_usage`         :ref:`enterprise-label`
========================================================== =======================

See :py:class:`~TheNounProjectAPI.api.API` for the other methods not listed here.

See `the Noun Project documentation <https://api.thenounproject.com/documentation.html>`_ for more information.

Output handling
^^^^^^^^^^^^^^^

Let's take a look at some examples of how to parse the outputs from the aforementioned methods.

.. _icons-code-label:

:ref:`Icons<icons-label>`
""""""""""""""""""""""""""""""""""""""""""

.. code-block:: python
    :lineno-start: 7

    # See Sample outputs -> Icons for more information about this: 
    icons = api.get_icons_by_term("goat", public_domain_only=True, limit=2)
    
    # >>>icons
    # [<IconModel: Term: Goat Feeding, Slug: goat-feeding, Id: 24014>, 
    # <IconModel: Term: Herbivore teeth, Slug: herbivore-teeth, Id: 675870>]

    for icon in icons:
        print("Icon's term:", icon.term)
        print("This icon's tags:", ", ".join(tag.slug for tag in icon.tags))
        print("Uploader's username:", icon.uploader.username)

.. _icon-code-label:

:ref:`Icon<icon-label>`
"""""""""""""""""""""""

.. code-block:: python
    :lineno-start: 7

    # See Sample outputs -> Icon for more information about this: 
    icon = api.get_icon("goat")
    
    # >>>icon
    # <IconModel: Term: Goat, Slug: goat, Id: 8786>

    print("Icon's term:", icon.term)
    print("This icon's tags:", ", ".join(tag.slug for tag in icon.tags))
    print("Uploader's username:", icon.uploader.username)

.. _collections-code-label:

:ref:`Collections<collections-label>`
"""""""""""""""""""""""""""""""""""""

.. code-block:: python
    :lineno-start: 7

    # See Sample outputs -> Collections for more information about this: 
    collections = api.get_collections(limit=3)
    
    # >>>collections
    # [<CollectionModel: Name: Electric, Slug: electric, Id: 88081>, 
    #  <CollectionModel: Name: Banking, Slug: banking, Id: 88080>, 
    #  <CollectionModel: Name: Academy, Slug: academy, Id: 88079>]

    for collection in collections:
        print("Collection's name:", collection.name)
        print("Collection's tags:", ", ".join(tag for tag in collection.tags))
        print("Author's username:", collection.author.username)

.. _collection-code-label:

:ref:`Collection<collection-label>`
"""""""""""""""""""""""""""""""""""

.. code-block:: python
    :lineno-start: 7

    # See Sample outputs -> Collection for more information about this: 
    collection = api.get_collection("goat")
    
    # >>>collection
    # <CollectionModel: Name: Goat, Slug: goat, Id: 6861>

    print("Collection's name:", collection.name)
    print("Collection's tags:", ", ".join(tag for tag in collection.tags))
    print("Author's username:", collection.author.username)

.. _usage-code-label:

:ref:`Usage<usage-label>`
"""""""""""""""""""""""""

.. code-block:: python
    :lineno-start: 7

    # See Sample outputs -> Usage for more information about this: 
    usage = api.get_usage()

    # >>>usage
    # <UsageModel: Hourly: 12, Daily: 12, Monthly: 226>

    print("Monthly limit:", usage.limits.monthly)
    print("Today's usage:", usage.usage.daily)

Exception handling
^^^^^^^^^^^^^^^^^^
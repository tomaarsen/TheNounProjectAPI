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

Handling outputs
^^^^^^^^^^^^^^^^

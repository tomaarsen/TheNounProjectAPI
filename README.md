[![Build Status](https://travis-ci.com/tomaarsen/TheNounProjectAPI.svg?branch=master)](https://travis-ci.com/tomaarsen/TheNounProjectAPI)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/tomaarsen/TheNounProjectAPI.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/tomaarsen/TheNounProjectAPI/context:python)
[![codecov](https://codecov.io/gh/tomaarsen/TheNounProjectAPI/branch/master/graph/badge.svg)](https://codecov.io/gh/tomaarsen/TheNounProjectAPI)
[![license](https://img.shields.io/github/license/tomaarsen/TheNounProjectAPI)](https://github.com/tomaarsen/TheNounProjectAPI/blob/master/LICENSE)

# TheNounProjectAPI
 
TheNounProjectAPI is a Python wrapper allowing convenient access to the [Noun Project](https://thenounproject.com/) API. It supports all endpoints and types of responses. Documentation for this wrapper can be found [here](https://tomaarsen.github.io/TheNounProjectAPI/#thenounprojectapi), while the official documentation of the API itself may be found [here](https://api.thenounproject.com/).

---

# Installation
TheNounProjectAPI is supported on Python 3.7+. The recommended method of installation is via [pip](https://pypi.org/project/pip/).
```
pip install TheNounProjectAPI
```
You can also install TheNounProjectAPI directly from github using:
```
pip install --upgrade https://github.com/tomaarsen/TheNounProjectAPI/archive/master.zip
```
For help with installing Python and/or pip, see "The Hitchhiker's Guide to Python" [Installation Guides](https://docs.python-guide.org/starting/installation/#installation-guides)

---

# Getting started
It's strongly encouraged to use the [documentation](https://tomaarsen.github.io/TheNounProjectAPI/#thenounprojectapi)'s [Getting started](https://tomaarsen.github.io/TheNounProjectAPI/introduction.html#getting-started) section to get started, as it's tied to the rest of the documentation, allowing you to quickly find exactly what you need.

However, I'll provide a quick sample.
```python
# See the Documentation for more information: https://tomaarsen.github.io/TheNounProjectAPI
from TheNounProjectAPI import API

if __name__ == "__main__":
    # API Key and Secret from https://api.thenounproject.com/getting_started.html#creating-an-api-key
    key = "<my api key>"
    secret = "<my api secret>"
    
    # Create api object
    api = API(key=key, secret=secret)

    # See the documentation for more endpoints
    icons = api.get_icons_by_term("goat", public_domain_only=True, limit=2)

    # >>>icons
    # [<IconModel: Term: Goat Feeding, Slug: goat-feeding, Id: 24014>,
    # <IconModel: Term: Herbivore teeth, Slug: herbivore-teeth, Id: 675870>]

    for icon in icons:
        print("Icon's term:", icon.term)
        print("This icon's tags:", ", ".join(tag.slug for tag in icon.tags))
        print("Uploader's username:", icon.uploader.username)
```

Examine the [TheNounProjectAPI documentation](https://tomaarsen.github.io/TheNounProjectAPI/index.html#thenounprojectapi) for more examples of what can be done with TheNounProjectAPI.

---

# Documentation
Documentation can be found here: https://tomaarsen.github.io/TheNounProjectAPI

---

# Tests
Run `python runner.py`, `nosetests`, `python setup.py nosetests` or `python setup.py test` to run all tests in one batch.

# License
TheNounProjectAPI is licensed under MIT.

# Contributions
Contributions are welcome.

# TheNounProjectAPI
 
TheNounProjectAPI is a Python wrapper allowing convenient access to the [Noun Project](https://thenounproject.com/) API. It supports all endpoints and types of responses. Documentation for this wrapper can be found [here](), while the official documentation of the API itself may be found [here](https://api.thenounproject.com/).

---

# Installation
TheNounProjectAPI is supported on Python 3.7+. The recommended method of installation is via [pip](https://pypi.org/project/pip/).
```
pip install TheNounProjectAPI
```
You can also install TheNounProjectAPI directly from github using:
```
pip install --upgrade https://github.com/CubieDev/TheNounProjectAPI/archive/master.zip
```
For help with installing Python and/or pip, see "The Hitchhiker's Guide to Python" [Installation Guides](https://docs.python-guide.org/starting/installation/#installation-guides)

---

# Getting started
It's strongly encouraged to use the [documentation]()'s [Getting started]() section to get started, as it's tied to the rest of the documentation, allowing you to quickly find exactly what you need.

However, I'll provide a quick sample.
```python
import TheNounProjectAPI

key = "<sample key>"
secret = "<sample secret>"

api = TheNounProjectAPI(key=key, secret=secret)

icons = api.get_icons_by_term("goat", public_domain_only=True, limit=2)

# >>>icons
# [<IconModel: Term: Goat Feeding, Slug: goat-feeding, Id: 24014>,
# <IconModel: Term: Herbivore teeth, Slug: herbivore-teeth, Id: 675870>]

for icon in icons:
    print("Icon's term:", icon.term)
    print("This icon's tags:", ", ".join(tag.slug for tag in icon.tags))
    print("Uploader's username:", icon.uploader.username)
```

Examine the [TheNounProjectAPI documentation]() for more examples of what can be done with TheNounProjectAPI.

---

# Tests
Run `run_tests.py` to run all tests in one batch.

# License
TheNounProjectAPI is licensed under MIT.

# Contributions
Contributions are welcome.

szamlazz.py
----
The **szamlazz.py** package is a Python client (wrapper) for *Szamlazz.hu::Számla Agent*.

# Introduction
Számla Agent is a non-browser-based interface of the Számlázz.hu system.
It receives XML messages and depending on the received information it can do various actions.

Using **szamlazz.py**, you can interact with this interface in a convenient and Pythonic way.

# Integration
Install the package from PyPI:
```shell
pip install szamlazz.py
```

Import the client into your Python module:
```python
from szamlazz import SzamlazzClient

# Depending on your future action(s), you might need the following model classes too:
from szamlazz import Header, Merchant, Buyer, Item, PdfDataMissingError
```
For all model classes, see [models.py](szamlazz/models.py).

# API
The `SzamlazzClient` instance can be initialised in two ways:
  * username/password combination
  * Agent Key (Számla Agent Kulcs)

Failing to provide one of these authentication methods will raise `AssertionError`.

All operations (e.g.: `generate_invoice`, `reverse_invoice`, etc.) return a new `SzamlazzResponse` instance.

Currently, the following operations can be executed via **szamlazz.py**:
  * create invoices
  * reverse invoices
  * ~~register credit entries~~
  * ~~query invoice pdf files~~
  * ~~query invoice xml files~~
  * ~~delete pro forma invoices~~
  * ~~create receipts~~
  * ~~reverse receipts~~
  * ~~query receipts~~
  * ~~send receipts~~
  * ~~query taxpayers~~
  * ~~perform self billing~~

New operations are continuously implemented. Contributions are welcome too.

# Contribution
Contributions are welcome. Should you have a question or an idea, open a new GitHub issue.
Your contributions are expected through GitHub Pull Requests.



## New Release
Make sure you have the latest version of PyPA’s build installed:
```shell
python -m pip install --upgrade build
```

Run this command from the same directory where `pyproject.toml` is located:
```shell
python setup.py sdist bdist_wheel
```

# License
MIT

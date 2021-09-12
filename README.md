szamlazz.py
----
The **szamlazz.py** package is a Python client (wrapper) for *Szamlazz.hu::Számla Agent*.

# Introduction
Számla Agent is a non-browser-based interface of the Számlázz.hu system.
It receives XML messages and depending on the received information it can do various actions.

Using **szamlazz.py**, you can interact with this interface in a convenient and Pythonic way.

**szamlazz.py** provides multiple translated (Hungarian -> English) `NamedTuple` classes to help interaction with the API client. 

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

All actions (e.g.: `generate_invoice`, `reverse_invoice`, etc.) return a new `SzamlazzResponse` instance. <br>
`SzamlazzResponse` has the following major parameters:
  * `.has_errors`
  * `.error_code`
  * `.error_message`
  * `.ok`
  * `.response`
  * `.text`

`SzamlazzResponse` has the following major functions:
  * `.get_pdf_base64()`
  * `.get_pdf_bytes()`
  * `.write_pdf_to_disk()`
  * `.print_errors()`

For more details, see the contents of [`class SzamlazzResponse`](szamlazz/models.py).

## Implementation Status
Currently, the following actions can be executed via **szamlazz.py**:
  * create invoices
  * reverse invoices
  * register credit entries
  * query invoice pdf files
  * query invoice xml files
  * delete pro forma invoices
  * create receipts // **With limitations. See the source code for more details**
  * reverse receipts
  * query receipts
  * send receipts
  * query taxpayers
  * ~~self billing~~ // **Implementation is not on the roadmap**

**Note:** New actions are continuously implemented. Contributions are welcome too.

Each action's function takes a definite number of arguments. For example, let's examine `SzamlazzClient.generate_invoice()`:
```python
from typing import List
from szamlazz.models import Header, Merchant, Buyer, Item, SzamlazzResponse

def generate_invoice(header: Header,
                     merchant: Merchant,
                     buyer: Buyer,
                     items: List[Item],
                     e_invoice: bool = True,
                     invoice_download: bool = True,
                     ) -> SzamlazzResponse:
    pass
```

The *Szamlazz.hu::Számla Agent* XML has the following tags (depending on the action):
```xml
<xmlszamla>
    <beallitasok></beallitasok>
    <fejlec></fejlec>
    <elado></elado>
    <vevo></vevo>
    <tetelek>
        <tetel></tetel>
    </tetelek>
</xmlszamla>
```

Each of these tags, except `<beallitasok>` and `<tetelek>` can be mapped to a dataclass model:
  * `fejlec` -> `Header`
  * `elado` -> `Merchant`
  * `vevo` -> `Buyer`
  * `tetel` -> `Item`

Use the models to create your payloads for each action, for example, to create a `<fejlec>`:
```python
from szamlazz.models import Header

fejlec = Header(
    creating_date="2021-08-26",
    payment_date="2021-08-26",
    due_date="2021-08-31",
    payment_type="Átutalás",
    currency="HUF",
    invoice_language="hu",
    invoice_comment="No Comment",
    name_of_bank="MNB",
    exchange_rate=0.0,
    order_number="ORDER-73",
    pro_forma_number_ref="",
    deposit_invoice=False,
    invoice_after_deposit_invoice=False,
    correction_invoice=False,
    number_of_corrected_invoice="",
    proforma_invoice=False,
    invoice_prefix="DK",
)
```

This `Header` dataclass instance can be passed to the `generate_invoice` function:
```python
resp = generate_invoice(header=fejlec)
```

# Contribution
Contributions are welcome. Should you have a question or an idea, open a new GitHub issue.
Your contributions are expected through GitHub Pull Requests.

If you're developing with PyCharm, consider using `examples/IntelliJ Config Template.run.xml` 
to configure the examples (demo files) for quick testing.

## Releasing
Releases are automatically pushed from the `master` branch on a new tag using [GitHub Workflows](.github/workflows/publish-to-pypi.yml).

**Manual Releasing** <br>
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

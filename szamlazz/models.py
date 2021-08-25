import base64
import logging
from pathlib import Path
from requests.models import Response
from typing import NamedTuple, Tuple
from urllib.parse import unquote
# noinspection PyPep8Naming
import xml.etree.ElementTree as ET

from szamlazz.utils import PdfDataMissingError


__all__ = ["Header", "Merchant", "Buyer", "Item", "SzamlazzResponse"]  # "WayBill"
logger = logging.getLogger(__name__)


class Header(NamedTuple):
    """<fejlec>"""
    creating_date: str = ""  # <keltDatum>2020-01-20</keltDatum>
    payment_date: str = ""  # <teljesitesDatum>2020-01-20</teljesitesDatum>
    due_date: str = ""  # <fizetesiHataridoDatum>2020-01-20</fizetesiHataridoDatum>
    payment_type: str = "Átutalás"  # <fizmod>Átutalás</fizmod>
    currency: str = "HUF"  # <penznem>HUF</penznem>
    invoice_language: str = "hu"  # <szamlaNyelve>hu</szamlaNyelve> // can  be: de, en, it, hu, fr, ro, sk, hr
    invoice_comment: str = ""  # <megjegyzes>Invoice comment</megjegyzes>
    name_of_bank: str = "MNB"  # <arfolyamBank>MNB</arfolyamBank>
    exchange_rate: float = 0.0  # <arfolyam>0.0</arfolyam>
    order_number: str = ""  # <rendelesSzam></rendelesSzam>
    pro_forma_number_ref: str = ""  # <dijbekeroSzamlaszam></dijbekeroSzamlaszam>
    deposit_invoice: bool = False  # <elolegszamla>false</elolegszamla>
    invoice_after_deposit_invoice: bool = False  # <vegszamla>false</vegszamla>
    correction_invoice: bool = False  # <helyesbitoszamla>false</helyesbitoszamla>
    number_of_corrected_invoice: str = ""  # <helyesbitettSzamlaszam></helyesbitettSzamlaszam>
    proforma_invoice: bool = False  # <dijbekero>false</dijbekero>
    invoice_prefix: str = ""  # <szamlaszamElotag></szamlaszamElotag>
    invoice_number: str = ""  # <szamlaszam>E-TST-2011-1</szamlaszam>  // needed for reverse_invoice|storno only
    invoice_template: str = ""  # <!-- Codomain: 'SzlaMost' | 'SzlaAlap' | 'SzlaNoEnv' | 'Szla8cm' | 'SzlaTomb' | 'SzlaFuvarlevelesAlap' -->


class Merchant(NamedTuple):
    """<elado>"""
    bank_name: str = ""  # <bank>BB</bank>
    bank_account_number: str = ""  # <bankszamlaszam>11111111-22222222-33333333</bankszamlaszam>
    reply_email_address: str = ""  # <emailReplyto> </emailReplyto>
    email_subject: str = ""  # <emailTargy>Invoice notification</emailTargy>
    email_text: str = ""  # <emailSzoveg>mail text</emailSzoveg>


class Buyer(NamedTuple):
    """<vevo>"""
    name: str = ""  # <nev>Kovacs Bt.</nev>
    zip_code: str = ""  # <irsz>2030</irsz>
    city: str = ""  # <telepules>Érd</telepules>
    address: str = ""  # <cim>Tárnoki út 23.</cim>
    email: str = ""  # <email>buyer@example.com</email>
    send_email: bool = False  # <sendEmail>false</sendEmail>
    tax_number: str = ""  # <adoszam>12345678-1-42</adoszam>
    tax_number_eu: str = ""  # <adoszamEU>HU55555555</adoszamEU>  // needed for reverse_invoice|storno only
    delivery_name: str = ""  # <postazasiNev>Kovács Bt. mailing name</postazasiNev>
    delivery_zip: str = ""  # <postazasiIrsz>2040</postazasiIrsz>
    delivery_city: str = ""  # <postazasiTelepules>Budaörs</postazasiTelepules>
    delivery_address: str = ""  # <postazasiCim>Szivárvány utca 8.</postazasiCim>
    identification: str = ""  # <azonosito>1234</azonosito>
    phone_number: str = ""  # <telefonszam>Tel:+3630-555-55-55, Fax:+3623-555-555</telefonszam>
    comment: str = ""  # <megjegyzes>Call extension 214 from the reception</megjegyzes>


# class WayBill(NamedTuple):
#     """<fuvarlevel>"""
#      <!-- waybill/confinement note, you do not need this: omit the entire tag -->
#     uticel: str = ""  #
#     futarSzolgalat: str = ""  #


class Item(NamedTuple):
    name: str = ""  # <megnevezes>Elado izé</megnevezes>
    quantity: str = ""  # <mennyiseg>1.0</mennyiseg>
    quantity_unit: str = ""  # <mennyisegiEgyseg>db</mennyisegiEgyseg>
    unit_price: str = ""  # <nettoEgysegar>10000</nettoEgysegar>
    vat_rate: str = ""  # <afakulcs>27</afakulcs>
    net_price: str = ""  # <nettoErtek>10000.0</nettoErtek>
    vat_amount: str = ""  # <afaErtek>2700.0</afaErtek>
    gross_amount: str = ""  # <bruttoErtek>12700.0</bruttoErtek>
    comment_for_item: str = ""  # <megjegyzes>lorem ipsum</megjegyzes>


class SzamlazzResponse:
    szamlazz_ns = "{http://www.szamlazz.hu/xmlszamlavalasz}"  # Szamlazz.hu response namespace

    def __init__(self, response: Response):
        self.__response = response
        content_type = response.headers.get("Content-Type")
        if content_type == "application/octet-stream":
            # Parse XML and map into class members
            root = ET.fromstring(self.__response.text)
            self.pdf: str = self.__get_tag_text(root, 'pdf')
            self.pdf_bytes: bytes = b''
        else:
            self.pdf: str = ""
            self.pdf_bytes: bytes = response.content

        # Error Handling
        self.error_code: str = response.headers.get("szlahu_error_code")
        self.error_message: str = response.headers.get("szlahu_error")
        if self.error_message:
            self.error_message = unquote(self.error_message)
        self.success: str = "false" if self.error_code else "true"

        # Extract Details
        self.invoice_number: str = response.headers.get("szlahu_szamlaszam")
        self.invoice_net_price: str = response.headers.get("szlahu_nettovegosszeg")
        self.invoice_gross_price: str = response.headers.get("szlahu_bruttovegosszeg")
        self.receivables: str = response.headers.get("szlahu_kintlevoseg")
        self.buyer_account_url: str = response.headers.get("szlahu_vevoifiokurl")
        if self.buyer_account_url:
            self.buyer_account_url = unquote(response.headers.get("szlahu_vevoifiokurl"))

        self.__has_errors = self.error_code or self.error_message
        if self.has_errors:
            logger.error(f'Error Code: {self.error_code}')
            logger.error(f'Error Message: {self.error_message}')

    @property
    def has_errors(self):
        return self.__has_errors

    @property
    def ok(self):
        """
        Shortcut to the original response's attribute with the same name
        """
        return self.__response.ok

    @property
    def response(self) -> Response:
        """
        Original HTTP Response object returned by the requests package
        :return: requests.models.Response
        """
        return self.__response

    @property
    def text(self) -> str:
        """
        Shortcut to the original response's attribute with the same name
        """
        return self.__response.text

    def get_pdf_base64(self) -> str:
        if (not self.pdf) and (not self.pdf_bytes):
            raise PdfDataMissingError('No PDF was returned. Check the value of szamlaLetoltes|invoice_download')
        return self.pdf

    def get_pdf_bytes(self) -> bytes:
        pdf_base64 = self.get_pdf_base64()
        return base64.b64decode(pdf_base64) if pdf_base64 else self.pdf_bytes

    def write_pdf_to_disk(self, pdf_output_path: Path):
        if not pdf_output_path.parent.exists():
            raise FileNotFoundError(f"Output file's parent folder is missing: {pdf_output_path.parent.as_posix()}")
        data = self.get_pdf_bytes()
        with open(pdf_output_path, 'wb+') as f:
            f.write(data)

    def print_details(self):
        if not self.has_errors:
            print('success:', self.success)
            print('invoice_number:', self.invoice_number)
            print('invoice_net_price:', self.invoice_net_price)
            print('invoice_gross_price:', self.invoice_gross_price)
            print('receivables:', self.receivables)
            print('buyer_account_url:', self.buyer_account_url)
        else:
            self.print_errors()

    def print_errors(self) -> Tuple[str, str]:
        """
        Prints the returned error_code and error_message
        :return: Tuple[error_code, error_message]
        """
        if self.has_errors:
            print('error_code:', self.error_code)
            print('error_message:', self.error_message)
        return self.error_code, self.error_message

    def __get_tag_text(self, root: ET.Element, tag_name):
        tag = root.find(f'{self.szamlazz_ns}{tag_name}')
        return tag.text if tag is not None else None

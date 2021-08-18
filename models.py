from typing import NamedTuple


__all__ = ["Header", "Seller", "Buyer", "WayBill", "Item"]


class Header(NamedTuple):
    """<fejlec>"""
    creating_date: str = ""  # <keltDatum>2020-01-20</keltDatum>
    payment_date: str = ""  # <teljesitesDatum>2020-01-20</teljesitesDatum>
    due_date: str = ""  # <fizetesiHataridoDatum>2020-01-20</fizetesiHataridoDatum>
    payment_type: str = "Átutalás"  # <fizmod>Átutalás</fizmod>
    currency: str = "HUF"  # <penznem>HUF</penznem>
    invoice_language: str = "hu"  # <szamlaNyelve>hu</szamlaNyelve>
    invoice_comment: str = ""  # <megjegyzes>Invoce comment</megjegyzes>
    name_of_bank: str = "MNB"  # <arfolyamBank>MNB</arfolyamBank>
    exchange_rate: float = 0.0  # <arfolyam>0.0</arfolyam>
    order_number: str = ""  # <rendelesSzam></rendelesSzam>
    pro_forma_number_ref: str = ""  # <dijbekeroSzamlaszam></dijbekeroSzamlaszam>
    deposit_invoice: bool = False  # <elolegszamla>false</elolegszamla>
    invoice_after_deposit_invoice: bool = False  # <vegszamla>false</vegszamla>
    correction_invoice: bool = False  # <helyesbitoszamla>false</helyesbitoszamla>
    number_of_corrected_invoice: str = ""  # <helyesbitettSzamlaszam></helyesbitettSzamlaszam>
    proforma_invoice: bool = False  #  <dijbekero>false</dijbekero>
    invoice_prefix: str = ""  #  <szamlaszamElotag></szamlaszamElotag>


class Seller(NamedTuple):
    bank_name: str = "BB"
    bank_account_number: str = ""
    reply_email_address: str = ""
    email_subject: str = ""
    email_text: str = ""


class Buyer(NamedTuple):
    pass


class WayBill(NamedTuple):
    pass


class Item(NamedTuple):
    name: str = ""
    quantity: str = ""
    quantity_unit: str = ""
    unit_price: str = ""
    vat_rate: str = ""
    net_price: str = ""
    vat_amount: str = ""
    gross_amount: str = ""
    comment_for_item: str = ""

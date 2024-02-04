import logging
from os import getenv
from pathlib import Path
from datetime import datetime

from szamlazz import SzamlazzClient, Header, Merchant, Buyer, Item, PdfDataMissingError


logging.basicConfig(format='%(asctime)s %(name)s[:%(lineno)d] %(funcName)s %(levelname)s: %(message)s', datefmt='%b %d %H:%M:%S')
logging.root.setLevel(logging.DEBUG)
TODAY = datetime.today()
TMP_FOLDER_PDF_FILES = Path("./.tmp/pdf_files")


if __name__ == '__main__':
    TMP_FOLDER_PDF_FILES.mkdir(parents=True, exist_ok=True)
    # noinspection SpellCheckingInspection
    client = SzamlazzClient(
        agent_key=getenv('agent_key'),
    )

    demo_header = Header(
        creating_date=TODAY.strftime("%Y-%m-%d"),
        payment_date=TODAY.strftime("%Y-%m-%d"),
        due_date=TODAY.strftime("%Y-%m-%d"),
        payment_type="Átutalás",
        currency="HUF",
        invoice_language="hu",
        invoice_comment="No Comment",
        name_of_bank="MNB",
        exchange_rate=0.0,
        order_number=f'ORDER-{TODAY.strftime("%m%d")}',
        pro_forma_number_ref="",
        deposit_invoice=False,
        invoice_after_deposit_invoice=False,
        correction_invoice=False,
        number_of_corrected_invoice="",
        proforma_invoice=False,
        invoice_prefix="DK",
    )

    demo_merchant = Merchant(
        bank_name="OTP",
        bank_account_number="11111111-22222222-33333333",
        reply_email_address="merchant+noreply@demomerchant.hu",
        email_subject="Invoice notification",
        email_text="mail text"
    )

    demo_buyer = Buyer(
        name="Kovacs Bt.",
        zip_code="2030",
        city="Érd",
        address="Tárnoki út 23.",
        email="buyer@example.com",
        tax_subject=0, # <!-- Possible values are 7:business is based outside of the European Union, 6:business is based in the Europen Union, 1: has a hungarian tax number, 0: we don't know, if the buyer has a tax number, -1: no tax number -->
        send_email=False,
        tax_number="12345678-1-42",
        delivery_name="Kovács Bt. mailing name",
        delivery_zip="2040",
        delivery_city="Budaörs",
        delivery_address="Szivárvány utca 8.",
        identification="1234",
        phone_number="Tel:+3630-555-55-55, Fax:+3623-555-555",
        comment="Call extension 214 from the reception",
    )

    item_1 = Item(
        name="Eladó izé 1 X",
        quantity="2.0",
        quantity_unit="db",
        unit_price="10000",
        vat_rate="27",
        net_price="20000.0",
        vat_amount="5400.0",
        gross_amount="25400.0",
        comment_for_item="lorem ipsum 2",
    )

    item_2 = Item(
        name="Eladó izé 2 X",
        quantity="2.0",
        quantity_unit="db",
        unit_price="10000",
        vat_rate="27",
        net_price="20000.0",
        vat_amount="5400.0",
        gross_amount="25400.0",
        comment_for_item="lorem ipsum 2X",
    )

    item_3 = Item(
        name="Eladó izé 3 X",
        quantity="2.0",
        quantity_unit="db",
        unit_price="10000",
        vat_rate="27",
        net_price="20000.0",
        vat_amount="5400.0",
        gross_amount="25400.0",
        comment_for_item="lorem ipsum 2X",
    )

    invoice_response = client.generate_invoice(
        header=demo_header,
        merchant=demo_merchant,
        buyer=demo_buyer,
        items=[item_1, item_2, item_3, ],
    )

    invoice_response.response.raise_for_status()  # check for HTTP transmission errors
    invoice_response.print_errors()  # check for szamlazz.py errors

    try:
        invoice_response.write_pdf_to_disk(TMP_FOLDER_PDF_FILES / f'{invoice_response.invoice_number}.invoice.pdf')
    except PdfDataMissingError as e:
        # TODO: Do something here
        raise e

# -*- coding: utf-8 -*-

import logging
from os import getenv
from pathlib import Path

from szamlazz import SzamlazzClient, Header, Merchant, Buyer, Item, PdfDataMissingError


logging.basicConfig(format='%(asctime)s %(name)s[:%(lineno)d] %(funcName)s %(levelname)s: %(message)s', datefmt='%b %d %H:%M:%S')
logging.root.setLevel(logging.DEBUG)


if __name__ == '__main__':
    # noinspection SpellCheckingInspection
    client = SzamlazzClient(
        agent_key=getenv('agent_key'),
        response_version=1,
    )

    demo_header = Header(
        invoice_number="E-DK-2021-10",
        creating_date="2021-08-26",
        payment_date="2021-08-26",

    )

    demo_merchant = Merchant(
        reply_email_address="merchant+noreply@demomerchant.hu",
        email_subject="Invoice notification",
        email_text="mail text"
    )

    demo_buyer = Buyer(
        email="buyer@example.com",
        tax_number="12345678-1-42",
        # tax_number_eu="HU55555555",
    )

    response = client.reverse_invoice(
        header=demo_header,
        merchant=demo_merchant,
        buyer=demo_buyer,
    )

    response.response.raise_for_status()  # check for HTTP transmission errors
    response.print_errors()  # check for szamlazz.py errors

    try:
        response.write_pdf_to_disk(Path(rf'D:\proj\szamlazz.py\.tmp\pdf_invoices\{response.invoice_number}.STORNO.pdf'))
    except PdfDataMissingError as e:
        raise e

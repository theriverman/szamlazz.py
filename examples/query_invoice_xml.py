import logging
from os import getenv
from pathlib import Path
from datetime import datetime

from szamlazz import SzamlazzClient, Disbursement, PdfDataMissingError


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

    query_invoice_xml_response = client.query_invoice_xml(
        invoice_number="E-DK-2021-17",
        pdf=True,
    )

    query_invoice_xml_response.response.raise_for_status()  # check for HTTP transmission errors
    query_invoice_xml_response.print_errors()  # check for szamlazz.py errors

    try:
        query_invoice_xml_response.write_pdf_to_disk(TMP_FOLDER_PDF_FILES / f'{query_invoice_xml_response.invoice_number}.invoiceXML.pdf')
    except PdfDataMissingError as e:
        # TODO: Do something here
        print("PdfDataMissingError...")
        pass

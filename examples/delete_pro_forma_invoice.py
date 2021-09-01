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

    action = client.delete_pro_forma_invoice(
        invoice_number="D-DK-3",
        # order_number="ASD-1",
    )

    action.response.raise_for_status()  # check for HTTP transmission errors
    action.print_errors()  # check for szamlazz.py errors

    if action.action_success:
        print("OK")
    else:
        print("NOK")

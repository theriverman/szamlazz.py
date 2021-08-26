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

    disbursement_1 = Disbursement(
        date=TODAY.strftime("%Y-%m-%d"),
        title="készpénz",
        amount=1337,
    )
    register_credit_entry_response = client.register_credit_entry(
        invoice_number="E-DK-2021-15",
        disbursements=[disbursement_1, ],
        additive=True,
    )

    register_credit_entry_response.response.raise_for_status()  # check for HTTP transmission errors
    register_credit_entry_response.print_errors()  # check for szamlazz.py errors

    try:
        register_credit_entry_response.write_pdf_to_disk(TMP_FOLDER_PDF_FILES / f'{register_credit_entry_response.invoice_number}.credit_entry.pdf')
    except PdfDataMissingError as e:
        # TODO: Do something here
        raise e

import logging
import json
from os import getenv
from pathlib import Path
from datetime import datetime
import xmltodict


from szamlazz import SzamlazzClient, Disbursement, PdfDataMissingError


logging.basicConfig(format='%(asctime)s %(name)s[:%(lineno)d] %(funcName)s %(levelname)s: %(message)s', datefmt='%b %d %H:%M:%S')
logging.root.setLevel(logging.INFO)


if __name__ == '__main__':
    # noinspection SpellCheckingInspection
    client = SzamlazzClient(
        agent_key=getenv('agent_key'),
    )

    # resp = client.query_taxpayer("00000000")
    resp = client.query_taxpayer("10886861")
    if resp.has_errors:
        err_code, err_msg = resp.print_errors()
    else:
        print(resp.to_dict)

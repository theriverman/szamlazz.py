import logging
import requests

from jinja2 import Template
from requests.models import Response
from typing import List

from szamlazz.models import Header, Merchant, Buyer, Item, SzamlazzResponse
from szamlazz.utils import template_xml


__all__ = ["SzamlazzClient", ]
logger = logging.getLogger(__name__)


class SzamlazzClient:
    url = "https://www.szamlazz.hu/szamla/"

    def __init__(self,
                 username: str = "",
                 password: str = "",
                 agent_key: str = "",
                 response_version: int = 2,
                 ):
        """
        :param username: Számlázz.hu user
        :param password: Számlázz.hu’s user password
        :param agent_key: Számlázz.hu / Számla Agent Kulcs (key)
        :param response_version: Text|PDF or XML+PDF answer.

        response_version options:
            - 1: gives a simple text or PDF as answer.
            - 2: xml answer, in case you asked for the PDF as well, it will be included in the XML with base64 coding.
        """
        self.username = username
        self.password = password
        self.agent_key = agent_key
        self.response_version = response_version

    @property
    def can_extract_pdf(self):
        return True if self.response_version == 2 else False

    def generate_invoice(self,
                         header: Header,
                         merchant: Merchant,
                         buyer: Buyer,
                         items: List[Item],
                         e_invoice: bool = True,
                         invoice_download: bool = True,
                         ) -> SzamlazzResponse:
        settings = self._get_settings_dict()
        settings['eszamla'] = e_invoice
        settings['szamlaLetoltes'] = invoice_download
        payload_xml = {
            "header": header,
            "merchant": merchant,
            "buyer": buyer,
            "items": items,
            **settings,  # see SzamlazzClient._get_settings_dict() for details
        }
        template = Template(template_xml)
        output = template.render(payload_xml)
        logger.debug('Rendered Template Output: ' + output)
        r = self._execute_request(payload_xml=output)
        response = SzamlazzResponse(r)
        logger.info(f'success = {response.success}')
        logger.info(f'invoice_number = {response.invoice_number}')
        logger.info(f'buyer_account_url = {response.buyer_account_url}')
        return response

    def reverse_invoice(self):
        pass

    def register_credit_entry(self):
        pass

    def query_invoice_pdf(self):
        pass

    def query_invoice_xml(self):
        pass

    def delete_pro_forma_invoice(self):
        pass

    def generate_receipt(self):
        pass

    def reverse_receipt(self):
        pass

    def query_receipt(self):
        pass

    def send_receipt(self):
        pass

    def query_taxpayers(self):
        pass

    def self_bill(self):
        pass

    def _get_settings_dict(self) -> dict:
        return {
            "felhasznalo": self.username,
            "jelszo": self.password,
            "szamlaagentkulcs": self.agent_key,
            "eszamla": True,
            "szamlaLetoltes": True,
            "valaszVerzio": self.response_version,
        }

    def _execute_request(self, payload_xml: str, payload_extra_attachments: dict = None) -> Response:
        payload = {'action-xmlagentxmlfile': payload_xml}
        payload.update(payload_extra_attachments) if payload_extra_attachments else None
        return requests.post(self.url, files=payload)
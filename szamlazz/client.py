import base64
import logging
import requests

from jinja2 import Template
from requests.models import Response
from typing import List

from szamlazz import xsd
from szamlazz.models import Header, Merchant, Buyer, Item, Disbursement, SzamlazzResponse
from szamlazz import templates


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

        # authentication guards
        if all(v == "" for v in [self.username, self.password, self.agent_key]):
            raise AssertionError("A username/password combination OR the Agent Key (Számla Agent Kulcs) must be provided during initialisation")
        if all(v != "" for v in [self.username, self.password, self.agent_key]):
            raise AssertionError("Only one authentication method is allowed")

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
        settings = self._get_basic_settings()
        settings['eszamla'] = e_invoice
        settings['szamlaLetoltes'] = invoice_download
        payload_xml = {
            "header": header,
            "merchant": merchant,
            "buyer": buyer,
            "items": items,
            **settings,  # see SzamlazzClient._get_basic_settings() for details
        }
        template = Template(templates.xml_generate_invoice)
        output = template.render(payload_xml)

        ok, err = xsd.validate(xml=output, xsd=xsd.xsd_generate_invoice)
        if not ok:
            raise xsd.ValidationError(f"XML validation failed: " + err)

        logger.debug('Rendered Template Output: ' + output)
        r = self._execute_request(action='action-xmlagentxmlfile', payload_xml=output)
        response = SzamlazzResponse(r)
        logger.info(f'success = {response.success}')
        logger.info(f'invoice_number = {response.invoice_number}')
        logger.info(f'buyer_account_url = {response.buyer_account_url}')
        return response

    def reverse_invoice(self,
                        header: Header,
                        merchant: Merchant,
                        buyer: Buyer,
                        e_invoice: bool = True,
                        invoice_download: bool = True,  # True = Generated PDF will be returned
                        invoice_download_copy: int = 1,  # 1=PDF copy | 2=original
                        ) -> SzamlazzResponse:
        """
        Reversing an invoice (storno)

        In case you request the creation of a paper-based (non-electronic) invoice and you've set `invoice_download` to `True`,
        you can indicate that you not only need the original version of the invoice but the copy in a single PDF as well.
        You can indicate this in the `invoice_download_copy` parameter:
          * 1: PDF copy
          * 2: original
        :param header: Header
        :param merchant: Merchant
        :param buyer: Buyer
        :param e_invoice: True if E-Invoice
        :param invoice_download: True to retrieve the generated PDF
        :param invoice_download_copy: 1 = PDF copy | 2 = Original PDF
        :return: SzamlazzResponse
        """
        settings = self._get_basic_settings()
        settings['eszamla'] = e_invoice
        settings['szamlaLetoltes'] = invoice_download
        settings['szamlaLetoltesPld'] = invoice_download_copy
        payload_xml = {
            "header": header,
            "merchant": merchant,
            "buyer": buyer,
            **settings,  # see SzamlazzClient._get_basic_settings() for details
        }
        template = Template(templates.xml_reverse_invoice)
        output = template.render(payload_xml)
        logger.debug('Rendered Template Output: ' + output)

        ok, err = xsd.validate(xml=output, xsd=xsd.xsd_reverse_invoice)
        if not ok:
            raise xsd.ValidationError(f"XML validation failed: " + err)

        r = self._execute_request(action='action-szamla_agent_st', payload_xml=output)
        response = SzamlazzResponse(r)
        logger.info(f'success = {response.success}')
        logger.info(f'invoice_number = {response.invoice_number}')
        logger.info(f'buyer_account_url = {response.buyer_account_url}')
        return response

    def register_credit_entry(self,
                              invoice_number: str,
                              disbursements: List[Disbursement],
                              additive: bool = False,
                              ) -> SzamlazzResponse:
        """
        Registering a credit entry.

        :raise ValueError: On more than 5 credit entries in disbursements: List[Disbursement]
        :param invoice_number: szamlaszam
        :param disbursements: List[Disbursement]
        :param additive: if it is True, then the former credit entries will be retained [default=False]
        :return: SzamlazzResponse
        """
        if len(disbursements) > 5:
            raise ValueError("You can register maximum of 5 credit entries")

        settings = self._get_basic_settings()
        settings['szamlaszam'] = invoice_number
        settings['additiv'] = additive
        payload_xml = {
            "disbursements": disbursements,
            **settings,  # see SzamlazzClient._get_basic_settings() for details
        }
        template = Template(templates.xml_credit_entry)
        output = template.render(payload_xml)
        logger.debug('Rendered Template Output: ' + output)

        ok, err = xsd.validate(xml=output, xsd=xsd.xsd_credit_entry)
        if not ok:
            raise xsd.ValidationError(f"XML validation failed: " + err)

        r = self._execute_request(action='action-szamla_agent_kifiz', payload_xml=output)
        response = SzamlazzResponse(r)
        logger.info(f'success = {response.success}')
        logger.info(f'invoice_number = {response.invoice_number}')
        logger.info(f'buyer_account_url = {response.buyer_account_url}')
        return response

    def query_invoice_pdf(self,
                          invoice_number: str,
                          ) -> SzamlazzResponse:
        """
        There are two different types of the requested pdf:
          * in the case of a regular, paper-based invoice, it contains the next copy, or it can be 1 or 2 copies in the case it has not been printed before, depending on the settings.
          * in the case of an e-invoice, there is no such thing as copies, so it will give the original version back.

        The type of response depends on the value of the <valaszVerzio> | <response_version> variable sent in the request.
          * if it is 1 or not set, the response will be a PDF file
          * if it is 2, the response will be an XML file

        :param invoice_number: szamlaszam
        :return: SzamlazzResponse
        """
        settings = self._get_basic_settings()
        settings['szamlaszam'] = invoice_number
        payload_xml = {
            **settings,  # see SzamlazzClient._get_basic_settings() for details
        }
        template = Template(templates.xml_query_invoice_pdf)
        output = template.render(payload_xml)
        logger.debug('Rendered Template Output: ' + output)

        ok, err = xsd.validate(xml=output, xsd=xsd.xsd_query_invoice_pdf)
        if not ok:
            raise xsd.ValidationError(f"XML validation failed: " + err)

        r = self._execute_request(action='action-szamla_agent_pdf', payload_xml=output)
        response = SzamlazzResponse(r)
        logger.info(f'success = {response.success}')
        logger.info(f'invoice_number = {response.invoice_number}')
        # logger.info(f'buyer_account_url = {response.buyer_account_url}')
        return response

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

    def _get_basic_settings(self) -> dict:
        return {
            "felhasznalo": self.username,
            "jelszo": self.password,
            "szamlaagentkulcs": self.agent_key,
            "eszamla": True,
            "szamlaLetoltes": True,
            "valaszVerzio": self.response_version,
        }

    def _execute_request(self, action: str, payload_xml: str, payload_extra_attachments: dict = None) -> Response:
        payload = {action: payload_xml}
        payload.update(payload_extra_attachments) if payload_extra_attachments else None
        return requests.post(self.url, files=payload)

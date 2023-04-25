import logging
from typing import List, Tuple

import requests
from jinja2 import Template
from requests.models import Response

from szamlazz import templates
from szamlazz import xsd
from szamlazz.models import Header, Merchant, Buyer, Item, Disbursement, SzamlazzResponse, EmailDetails

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
        """
        https://docs.szamlazz.hu/#generating-invoices
        :param header: Header
        :param merchant: Merchant
        :param buyer: Buyer
        :param items: List[Item]
        :param e_invoice: bool (default=True)
        :param invoice_download: bool (default=True)
        :return: SzamlazzResponse
        """
        settings = self.get_basic_settings()
        settings["eszamla"] = e_invoice
        settings["szamlaLetoltes"] = invoice_download
        payload_xml = {
            "header": header,
            "merchant": merchant,
            "buyer": buyer,
            "items": items,
            **settings,  # see SzamlazzClient.get_basic_settings() for details
        }
        r = self.request_maker(
            action="action-xmlagentxmlfile",
            template=templates.generate_invoice,
            template_data=payload_xml,
            xsd_xml=xsd.generate_invoice,
        )
        response = SzamlazzResponse(r, xml_namespace="{http://www.szamlazz.hu/xmlszamlavalasz}")
        logger.info(f"success = {response.http_request_success}")
        logger.info(f"invoice_number = {response.invoice_number}")
        logger.info(f"buyer_account_url = {response.buyer_account_url}")
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
        settings = self.get_basic_settings()
        settings["eszamla"] = e_invoice
        settings["szamlaLetoltes"] = invoice_download
        settings["szamlaLetoltesPld"] = invoice_download_copy
        payload_xml = {
            "header": header,
            "merchant": merchant,
            "buyer": buyer,
            **settings,  # see SzamlazzClient.get_basic_settings() for details
        }
        r = self.request_maker(
            action="action-szamla_agent_st",
            template=templates.reverse_invoice,
            template_data=payload_xml,
            xsd_xml=xsd.reverse_invoice,
        )
        response = SzamlazzResponse(r, xml_namespace="")
        logger.info(f"success = {response.http_request_success}")
        logger.info(f"invoice_number = {response.invoice_number}")
        logger.info(f"buyer_account_url = {response.buyer_account_url}")
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

        settings = self.get_basic_settings()
        settings["szamlaszam"] = invoice_number
        settings["additiv"] = additive
        payload_xml = {
            "disbursements": disbursements,
            **settings,  # see SzamlazzClient.get_basic_settings() for details
        }
        r = self.request_maker(
            action="action-szamla_agent_kifiz",
            template=templates.credit_entry,
            template_data=payload_xml,
            xsd_xml=xsd.credit_entry,
        )
        response = SzamlazzResponse(r, xml_namespace="")
        logger.info(f"success = {response.http_request_success}")
        logger.info(f"invoice_number = {response.invoice_number}")
        logger.info(f"buyer_account_url = {response.buyer_account_url}")
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
        settings = self.get_basic_settings()
        settings["szamlaszam"] = invoice_number
        r = self.request_maker(
            action="action-szamla_agent_pdf",
            template=templates.query_invoice_pdf,
            template_data=settings,
            xsd_xml=xsd.query_invoice_pdf,
        )
        response = SzamlazzResponse(r, xml_namespace="{http://www.szamlazz.hu/xmlszamlavalasz}")
        logger.info(f"success = {response.http_request_success}")
        logger.info(f"invoice_number = {response.invoice_number}")
        return response

    def query_invoice_xml(self,
                          invoice_number: str = "",
                          order_number: str = "",
                          pdf: bool = True,
                          ) -> SzamlazzResponse:
        """
        Order number can be used in the query. In this case the last receipt with this order number will be returned

        :param invoice_number: szamlaszam
        :param order_number: rendelesSzam
        :param pdf: pdf
        :return: SzamlazzResponse
        """
        if invoice_number == "" and order_number == "":
            raise AssertionError("invoice_number OR order_number must be provided")

        settings = self.get_basic_settings()
        settings["szamlaszam"] = invoice_number
        settings["rendelesSzam"] = order_number
        settings["pdf"] = pdf
        r = self.request_maker(
            action="action-szamla_agent_xml",
            template=templates.query_invoice_xml,
            template_data=settings,
            xsd_xml=xsd.query_invoice_xml

        )
        response = SzamlazzResponse(r, xml_namespace="{http://www.szamlazz.hu/szamla}")
        logger.info(f"success = {response.http_request_success}")
        logger.info(f"invoice_number = {response.invoice_number}")
        return response

    def delete_pro_forma_invoice(self,
                                 invoice_number: str = "",
                                 order_number: str = "",
                                 ) -> SzamlazzResponse:
        """
        Order number can be used in the query. In this case the last receipt with this order number will be returned

        https://docs.szamlazz.hu/#deleting-a-pro-forma-invoice

        :param invoice_number: szamlaszam - pro forma invoice's unique number
        :param order_number: rendelesszam - manually added to the pro forma invoice upon generation
        :return: SzamlazzResponse
        """
        if invoice_number == "" and order_number == "":
            raise AssertionError("invoice_number OR order_number must be provided")

        settings = self.get_basic_settings()
        settings["szamlaszam"] = invoice_number
        settings["rendelesszam"] = order_number
        r = self.request_maker(
            action="action-szamla_agent_dijbekero_torlese",
            template=templates.delete_pro_forma_invoice,
            template_data=settings,
            xsd_xml=xsd.delete_pro_forma_invoice,
        )
        response = SzamlazzResponse(r, xml_namespace="{http://www.szamlazz.hu/xmlszamladbkdelvalasz}")
        logger.info(f"success = {response.http_request_success}")
        logger.info(f"invoice_number = {response.invoice_number}")
        return response

    def generate_receipt(self, payload: dict) -> Response:
        """
        https://docs.szamlazz.hu/#generating-a-receipt

        Key details from https://docs.szamlazz.hu/#expected-results-of-generating-receipts
        Every successful call contains the <sikeres>true</sikeres> field in the response.
        In case the generation of the receipt fails and the result field is false: <sikeres>false</sikeres>,
        two additional fields will be included in the response, <hibakod/> for the error code and <hibauzenet/> for the error message itself.

        Note: You should use hivasAzonosito to make the call fault tolerant.
              If this field is in use, it needs to be unique, otherwise the API call will be unsuccessful.
              This ensures that if the same XML is posted multiple times, it will not duplicate an existing receipt.

        :payload: dict
        :return: requests.models.Response
        """

        # language=Python
        """
from szamlazz import SzamlazzClient

client = SzamlazzClient(
agent_key="ASD123",
)
settings = client.get_basic_settings()
fejlec = {
    "hivasAzonosito": "",
    "elotag": "",
    "fizmod": "",
    "penznem": "",
    "devizabank": "",
    "devizaarf": "",
    "megjegyzes": "",
    "pdfSablon": "",
    "fokonyvVevo": "",
}
tetel_1 = {
    "megnevezes": "",
    "azonosito": "",
    "mennyiseg": "",
    "mennyisegiEgyseg": "",
    "nettoEgysegar": "",
    "netto": "",
    "afakulcs": "",
    "afa": "",
    "brutto": "",
    "fokonyv_arbevetel": "",
    "fokonyv_afa": "",
}
payload = {
    "fejlec": fejlec,
    "tetelek": [tetel_1, ],
    **settings
}

# pass payload to generate_receipt(payload=payload)
        """

        return self.request_maker(
            action="action-szamla_agent_nyugta_create",
            template=templates.generate_receipt,
            template_data=payload,
            xsd_xml=xsd.generate_receipt,
        )

    def reverse_receipt(self,
                        receipt_number: str,
                        pdf_template: str = "",
                        ) -> SzamlazzResponse:
        """
        https://docs.szamlazz.hu/#reversing-a-receipt-storno
        :param receipt_number: [string] <nyugtaszam>
        :param pdf_template: <pdfSablon>
        :return: SzamlazzResponse
        """
        settings = self.get_basic_settings()
        settings["nyugtaszam"] = receipt_number
        settings["pdfSablon"] = pdf_template
        r = self.request_maker(
            action="action-szamla_agent_nyugta_storno",
            template=templates.reverse_receipt,
            template_data=settings,
            xsd_xml=xsd.reverse_receipt,
        )
        response = SzamlazzResponse(r, xml_namespace="{http://www.szamlazz.hu/xmlnyugtavalasz}")
        logger.info(f"success = {response.http_request_success}")
        logger.info(f"invoice_number = {response.invoice_number}")
        logger.info(f"buyer_account_url = {response.buyer_account_url}")
        return response

    def query_receipt(self,
                      receipt_number: str,
                      pdf_template: str = "",
                      ) -> SzamlazzResponse:
        """
        https://docs.szamlazz.hu/#querying-a-receipt
        :param receipt_number: [string] <nyugtaszam>
        :param pdf_template: <pdfSablon>
        :return: SzamlazzResponse
        """
        settings = self.get_basic_settings()
        settings["nyugtaszam"] = receipt_number
        settings["pdfSablon"] = pdf_template
        r = self.request_maker(
            action="action-szamla_agent_nyugta_get",
            template=templates.query_receipt,
            template_data=settings,
            xsd_xml=xsd.query_receipt,
        )
        response = SzamlazzResponse(r, xml_namespace="{http://www.szamlazz.hu/xmlnyugtavalasz}")
        logger.info(f"success = {response.http_request_success}")
        logger.info(f"invoice_number = {response.invoice_number}")
        logger.info(f"buyer_account_url = {response.buyer_account_url}")
        return response

    def send_receipt(self,
                     email_details: EmailDetails,
                     send_again_previous_email: bool = False,
                     ) -> SzamlazzResponse:
        """
        https://docs.szamlazz.hu/#sending-a-receipt

        In case you would like to provide multiple e-mail addresses in the e-mail field of the XML file, they must be separated by “,” (comma).
        Example:
        email_details.addresses = "abc@domain.com,def@domain.com,ghi@domain.com"

        :param email_details: [EmailDetails]
        :param send_again_previous_email: if True, the previous e-mail will be sent
        :return: SzamlazzResponse
        """
        settings = self.get_basic_settings()
        payload = {
            "email_details": email_details,
            "sendAgainPreviousEmail": send_again_previous_email,
            **settings,
        }
        r = self.request_maker(
            action="action-szamla_agent_nyugta_send",
            template=templates.send_receipt,
            template_data=payload,
            xsd_xml=xsd.send_receipt,
        )
        response = SzamlazzResponse(r, xml_namespace="{http://www.szamlazz.hu/xmlnyugtasendvalasz}")
        logger.info(f"success = {response.http_request_success}")
        logger.info(f"invoice_number = {response.invoice_number}")
        logger.info(f"buyer_account_url = {response.buyer_account_url}")
        return response

    def query_taxpayer(self,
                       vat_number: str
                       ) -> Tuple[Response, str]:
        """
        This interface is used to query the validity of a VAT number. The data is from the Online Invoice Platform of NAV, the Hungarian National Tax and Customs Administration.

        The response always matches the QueryTaxPayerResponse type of Online Invoice Platform of NAV, the Hungarian National Tax and Customs Administration.
        xmlns="http://schemas.nav.gov.hu/OSA/2.0/api"
        xmlns:ns2="http://schemas.nav.gov.hu/OSA/2.0/data"

        https://docs.szamlazz.hu/#querying-taxpayers
        :param vat_number: [str] VAT Number of the queried company
        :return: Tuple[requests.models.Response, requests.models.Response.text]: (Response, returned XML string)
        """
        settings = self.get_basic_settings()
        payload = {
            "vat_number": vat_number,
            **settings,
        }
        r = self.request_maker(
            action="action-szamla_agent_taxpayer",
            template=templates.tax_payer,
            template_data=payload,
            xsd_xml=xsd.tax_payer,
        )
        return r, r.text

    def self_bill(self):
        raise NotImplementedError

    def request_maker(self, action: str, template: str, template_data: dict, xsd_xml: str = "", payload_extra_attachments: dict = None) -> Response:
        """
        Custom, non-managed requests can be made against SzámlaAgent.
        :param action: eg.: action-xmlagentxmlfile
        :param template: a Jinja2 compatible template XML string
        :param template_data: (dict) Data injected into the Jinja2 compatible template XML template
        :param xsd_xml: [optional] The XSD Scheme for XSD scheme compliance check
        :param payload_extra_attachments: (dict) Extra data injected into the Jinja2 compatible template XML template
        :return: requests.models.Response

        Note: Use SzamlazzClient.get_basic_settings() as a skeleton while creating your own template_data. See `get_basic_settings` to learn what fields are available automatically
        """
        t = Template(template)
        output = t.render(template_data)
        logger.debug(f"request_maker / action: {action}")
        logger.debug(f"request_maker / template: {template}")
        logger.debug(f"request_maker / template_data: {template_data}")
        logger.debug(f"request_maker / xsd_xml: {xsd_xml}")
        logger.debug(f"request_maker / Rendered Template Output: {output}")

        if xsd_xml != "":
            ok, err = xsd.validate(xml=output, xsd=xsd_xml)
            if not ok:
                raise xsd.ValidationError(f"XML validation failed: " + err)

        payload = {action: output}
        payload.update(payload_extra_attachments) if payload_extra_attachments else None
        return requests.post(self.url, files=payload)

    def get_basic_settings(self) -> dict:
        """
        get_basic_settings returns a dict containing the following key/value pairs:
          * felhasznalo
          * jelszo
          * szamlaagentkulcs
          * eszamla
          * szamlaLetoltes
          * valaszVerzio

        The values of these keys are dynamically taken from SzamlazzClient.
        :return: dict
        """
        return {
            "felhasznalo": self.username,
            "jelszo": self.password,
            "szamlaagentkulcs": self.agent_key,
            "eszamla": True,
            "szamlaLetoltes": True,
            "valaszVerzio": self.response_version,
        }

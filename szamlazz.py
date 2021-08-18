import requests
import requests.exceptions
from typing import List

from models import Header, Seller, Buyer, WayBill, Item


url = "https://www.szamlazz.hu/szamla/"
generate_invoice = "action-xmlagentxmlfile"
valaszVerzio = 1


class SzamlazzClient:
    def __init__(self,
                 username: str = "",
                 password: str = "",
                 agent_key: str = "",
                 e_invoice: bool = True,
                 invoice_download: bool = True,
                 response_type: int = 2,
                 ):
        """
        :param username: Számlázz.hu user
        :param password: Számlázz.hu’s user password
        :param agent_key: Számlázz.hu / Számla Agent Kulcs (key)
        """
        self.username = username
        self.password = password
        self.agent_key = agent_key
        self.e_invoice = e_invoice
        self.invoice_download = invoice_download
        self.response_type = response_type

    def generate_invoice(self,
                         header: Header,
                         seller: Seller,
                         buyer: Buyer,
                         waybill: WayBill,
                         items: List[Item]
                         ):
        pass

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

    def _execute_request(self):
        pass


if __name__ == '__main__':
    # DEMO RUN
    with open('teszt.xml', 'r', encoding="utf8") as f:
        payload_xml = f.read()

    values = { }
    files = {
        'action-xmlagentxmlfile': open('teszt.xml', 'r', encoding="utf8")
    }

    r = requests.post(url, files=files, data=values)
    print(r.text)

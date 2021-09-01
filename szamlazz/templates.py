__all__ = ["generate_invoice", "reverse_invoice", "credit_entry", "query_invoice_pdf", ]


# language=XML
generate_invoice: str = """<?xml version="1.0" encoding="UTF-8"?>
<xmlszamla xmlns="http://www.szamlazz.hu/xmlszamla"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://www.szamlazz.hu/xmlszamla https://www.szamlazz.hu/szamla/docs/xsds/agent/xmlszamla.xsd">
    <beallitasok>
        <felhasznalo>{{ felhasznalo }}</felhasznalo>
        <jelszo>{{ jelszo }}</jelszo>
        <szamlaagentkulcs>{{ szamlaagentkulcs }}</szamlaagentkulcs>
        <eszamla>{{ eszamla | lower }}</eszamla>
        <szamlaLetoltes>{{ szamlaLetoltes | lower }}</szamlaLetoltes>
        <valaszVerzio>{{ valaszVerzio }}</valaszVerzio>
        <aggregator>
        </aggregator>
    </beallitasok>
    <fejlec>
        <keltDatum>{{ header.creating_date }}</keltDatum>
        <teljesitesDatum>{{ header.payment_date }}</teljesitesDatum>
        <fizetesiHataridoDatum>{{ header.due_date }}</fizetesiHataridoDatum>
        <fizmod>{{ header.payment_type }}</fizmod>
        <penznem>{{ header.currency }}</penznem>
        <szamlaNyelve>{{ header.invoice_language }}</szamlaNyelve>
        <megjegyzes>{{ header.invoice_comment }}</megjegyzes>
        <arfolyamBank>{{ header.name_of_bank }}</arfolyamBank>
        <arfolyam>{{ header.exchange_rate }}</arfolyam>
        <rendelesSzam>{{ header.order_number }}</rendelesSzam>
        <dijbekeroSzamlaszam>{{ header.pro_forma_number_ref }}</dijbekeroSzamlaszam>
        <elolegszamla>{{ header.deposit_invoice | lower }}</elolegszamla>
        <vegszamla>{{ header.invoice_after_deposit_invoice | lower }}</vegszamla>
        <helyesbitoszamla>{{ header.correction_invoice | lower }}</helyesbitoszamla>
        <helyesbitettSzamlaszam>{{ header.number_of_corrected_invoice }}</helyesbitettSzamlaszam>
        <dijbekero>{{ header.proforma_invoice | lower }}</dijbekero>
        <szamlaszamElotag>{{ header.invoice_prefix }}</szamlaszamElotag>
    </fejlec>
    <elado>
        <bank>{{ merchant.bank_name }}</bank>
        <bankszamlaszam>{{ merchant.bank_account_number }}</bankszamlaszam>
        <emailReplyto>{{ merchant.reply_email_address }}</emailReplyto>
        <emailTargy>{{ merchant.email_subject }}</emailTargy>
        <emailSzoveg>{{ merchant.email_text }}</emailSzoveg>
    </elado>
    <vevo>
        <nev>{{ buyer.name }}</nev>
        <irsz>{{ buyer.zip_code }}</irsz>
        <telepules>{{ buyer.city }}</telepules>
        <cim>{{ buyer.address }}</cim>
        <email>{{ buyer.email }}</email>
        <sendEmail>{{ buyer.send_email | lower }}</sendEmail>
        <adoszam>{{ buyer.tax_number }}</adoszam>
        <postazasiNev>{{ buyer.delivery_name }}</postazasiNev>
        <postazasiIrsz>{{ buyer.delivery_zip }}</postazasiIrsz>
        <postazasiTelepules>{{ buyer.delivery_city }}</postazasiTelepules>
        <postazasiCim>{{ buyer.delivery_address }}</postazasiCim>
        <azonosito>{{ buyer.identification }}</azonosito>
        <telefonszam>{{ buyer.phone_number }}</telefonszam>
        <megjegyzes>{{ buyer.comment }}</megjegyzes>
    </vevo>
    <fuvarlevel>
        <uticel> </uticel>
        <futarSzolgalat> </futarSzolgalat>
    </fuvarlevel>
    <tetelek>
    {%- for item in items %}
        <tetel>
            <megnevezes>{{ item.name }}</megnevezes>
            <mennyiseg>{{ item.quantity }}</mennyiseg>
            <mennyisegiEgyseg>{{ item.quantity_unit }}</mennyisegiEgyseg>
            <nettoEgysegar>{{ item.unit_price }}</nettoEgysegar>
            <afakulcs>{{ item.vat_rate }}</afakulcs>
            <nettoErtek>{{ item.net_price }}</nettoErtek>
            <afaErtek>{{ item.vat_amount }}</afaErtek>
            <bruttoErtek>{{ item.gross_amount }}</bruttoErtek>
            <megjegyzes>{{ item.comment_for_item }}</megjegyzes>
        </tetel>
    {% endfor -%}
    </tetelek>
</xmlszamla>
"""

# language=XML
reverse_invoice = """<?xml version="1.0" encoding="UTF-8"?>
<xmlszamlast xmlns="http://www.szamlazz.hu/xmlszamlast"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://www.szamlazz.hu/xmlszamlast https://www.szamlazz.hu/szamla/docs/xsds/agentst/xmlszamlast.xsd">
    <beallitasok>
        <felhasznalo>{{ felhasznalo }}</felhasznalo>
        <jelszo>{{ jelszo }}</jelszo>
        <szamlaagentkulcs>{{ szamlaagentkulcs }}</szamlaagentkulcs>
        <eszamla>{{ eszamla | lower }}</eszamla>
        <szamlaLetoltes>{{ szamlaLetoltes | lower }}</szamlaLetoltes>
        <szamlaLetoltesPld>{{ szamlaLetoltesPld }}</szamlaLetoltesPld>
        <valaszVerzio>{{ valaszVerzio }}</valaszVerzio>
    </beallitasok>
    <fejlec>
        <szamlaszam>{{ header.invoice_number }}</szamlaszam>
        <keltDatum>{{ header.creating_date }}</keltDatum>
        <teljesitesDatum>{{ header.payment_date }}</teljesitesDatum>
        <tipus>SS</tipus>
        <szamlaSablon>{{ header.invoice_template }}</szamlaSablon>  <!-- Codomain: 'SzlaMost' | 'SzlaAlap' | 'SzlaNoEnv' | 'Szla8cm' | 'SzlaTomb' | 'SzlaFuvarlevelesAlap' -->
    </fejlec>
    <elado>
        <emailReplyto>{{ merchant.reply_email_address }}</emailReplyto>
        <emailTargy>{{ merchant.email_subject }}</emailTargy>
        <emailSzoveg>{{ merchant.email_text }}</emailSzoveg>
    </elado>
    <vevo>
        <email>{{ buyer.email }}</email>
        <adoszam>{{ buyer.tax_number }}</adoszam>
        <adoszamEU>{{ buyer.tax_number_eu }}</adoszamEU>
    </vevo>
</xmlszamlast>"""

# language=XML
credit_entry = """<?xml version="1.0" encoding="UTF-8"?>
<xmlszamlakifiz xmlns="http://www.szamlazz.hu/xmlszamlakifiz"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xsi:schemaLocation="http://www.szamlazz.hu/xmlszamlakifiz https://www.szamlazz.hu/szamla/docs/xsds/agentkifiz/xmlszamlakifiz.xsd">
  <beallitasok> <!-- settings -->
    <felhasznalo>{{ felhasznalo }}</felhasznalo>
    <jelszo>{{ jelszo }}</jelszo>
    <szamlaagentkulcs>{{ szamlaagentkulcs }}</szamlaagentkulcs>
    <szamlaszam>{{ szamlaszam }}</szamlaszam>
    <additiv>{{ additiv | lower }}</additiv>
  </beallitasok>
  {%- for disbursement in disbursements %}
  <kifizetes>
    <datum>{{ disbursement.date }}</datum>
    <jogcim>{{ disbursement.title }}</jogcim>
    <osszeg>{{ disbursement.amount }}</osszeg>
    <leiras>{{ disbursement.description }}</leiras>
  </kifizetes>
  {% endfor -%}
</xmlszamlakifiz>"""


# language=XML
query_invoice_pdf = """<?xml version="1.0" encoding="UTF-8"?>
<xmlszamlapdf xmlns="http://www.szamlazz.hu/xmlszamlapdf"
              xmlns:xsi="http://www.w3.org/2001/XMLSchemainstance"
              >
  <felhasznalo>{{ felhasznalo }}</felhasznalo>
  <jelszo>{{ jelszo }}</jelszo>
  <szamlaagentkulcs>{{ szamlaagentkulcs }}</szamlaagentkulcs>
  <szamlaszam>{{ szamlaszam }}</szamlaszam>
  <valaszVerzio>{{ valaszVerzio }}</valaszVerzio>
</xmlszamlapdf>
"""


# language=XML
query_invoice_xml = """<?xml version="1.0" encoding="UTF-8"?>
<xmlszamlaxml xmlns="http://www.szamlazz.hu/xmlszamlaxml"
              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
              xsi:schemaLocation="http://www.szamlazz.hu/xmlszamlaxml https://www.szamlazz.hu/szamla/docs/xsds/agentxml/xmlszamlaxml.xsd">
  <felhasznalo>{{ felhasznalo }}</felhasznalo>
  <jelszo>{{ jelszo }}</jelszo>
  <szamlaagentkulcs>{{ szamlaagentkulcs }}</szamlaagentkulcs>
  {% if rendelesSzam | length %}
  <rendelesSzam>{{ rendelesSzam }}</rendelesSzam>
  {% else %}
  <szamlaszam>{{ szamlaszam }}</szamlaszam>
  {% endif %}
  <pdf>{{ pdf | lower }}</pdf>
 </xmlszamlaxml>
"""

# language=XML
delete_pro_forma_invoice = """<?xml version="1.0" encoding="UTF-8"?>
<xmlszamladbkdel xmlns="http://www.szamlazz.hu/xmlszamladbkdel"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://www.szamlazz.hu/xmlszamladbkdel http://www.szamlazz.hu/docs/xsds/szamladbkdel/xmlszamladbkdel.xsd">
  <beallitasok>
    <felhasznalo>{{ felhasznalo }}</felhasznalo>
    <jelszo>{{ jelszo }}</jelszo>
    <szamlaagentkulcs>{{ szamlaagentkulcs }}</szamlaagentkulcs>
  </beallitasok>
  <fejlec>
    {% if rendelesszam | length %}
    <rendelesszam>{{ rendelesszam }}</rendelesszam>
    {% else %}
    <szamlaszam>{{ szamlaszam }}</szamlaszam>
    {% endif %}
  </fejlec>
</xmlszamladbkdel>"""


# language=XML
generate_receipt = """<?xml version="1.0" encoding="UTF-8"?>
<xmlnyugtacreate xmlns="http://www.szamlazz.hu/xmlnyugtacreate" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.szamlazz.hu/xmlnyugtacreate http://www.szamlazz.hu/docs/xsds/nyugta/xmlnyugtacreate.xsd">
  <beallitasok>                                                      <!-- REQ         -->
    <felhasznalo>Test123</felhasznalo>      <!-- REQ string  --> <!--user login name -->
    <jelszo>Test123</jelszo>                      <!-- REQ string  --> <!-- user password -->
    <szamlaagentkulcs>Please fill!</szamlaagentkulcs>
    <pdfLetoltes>false</pdfLetoltes>                       <!-- REQ boolean --> <!-- PDF download -->
  </beallitasok>
  <fejlec>                                                <!-- REQ         -->
    <hivasAzonosito></hivasAzonosito>     <!--     string  --> <!-- unique identifier of the call, duplication must be avoided-->
    <elotag>NYGTA</elotag>                    <!-- REQ string  --> <!-- receipt number prefix, required ==> NYGTA-2017-111 -->
    <fizmod>készpénz</fizmod>               <!-- REQ string  --> <!-- payment method, free text field, values ​​used on the interface are: átutalás, készpénz, bankkártya, csekk, utánvét, ajándékutalvány, barion, barter, csoportos beszedés, OTP Simple, kompenzáció, kupon, PayPal,PayU, SZÉP kártya, utalvány -->
    <penznem>Ft</penznem>                   <!-- REQ string  --> <!-- currency: Ft, HUF, EUR, USD stb. -->
    <devizabank>MNB</devizabank>         <!--     string  --> <!-- in case of foreign bill (not Ft/HUF) the name of the Bank -->
    <devizaarf>0.0</devizaarf>                 <!--     string  --> <!-- exchange rate -->
    <megjegyzes></megjegyzes>             <!--     string  --> <!-- free text description,  shown on the receipt -->
    <pdfSablon></pdfSablon>                   <!--     string  --> <!--  in case of custom PDF template, the identifier of the used template-->
    <fokonyvVevo></fokonyvVevo>                      <!--     string  --> <!-- general ledger ID of the customer -->
  </fejlec>
  <tetelek>                                        <!-- REQ         -->
    <tetel>                                         <!-- REQ         --> <!-- at least one item is required to issue a receipt  -->
      <megnevezes>Kitten doormat</megnevezes>         <!-- REQ string  --> <!-- name of the receipt -->
      <azonosito></azonosito>                                        <!--     string  --> <!-- ID of the receipt -->
      <mennyiseg>2.0</mennyiseg>                               <!-- REQ double  --> <!-- item quantity -->
      <mennyisegiEgyseg>db</mennyisegiEgyseg>          <!-- REQ string  --> <!-- unit of quantity -->
      <nettoEgysegar>10000</nettoEgysegar>                <!-- REQ double  --> <!-- net unit price -->
      <netto>20000.0</netto>                                 <!-- REQ double  --> <!-- net value (quantity * net unit price) -->
      <afakulcs>27</afakulcs>                                 <!-- REQ string  --> <!-- VAT rate, values: 0, 5, 10, 27, AAM, TAM, EU, EUK, MAA, F.AFA, K.AFA, ÁKK,HO, EUE, EUFADE, EUFAD37, ATK, NAM, EAM, KBAUK, KBAET -->
      <afa>5400.0</afa>                                                <!-- REQ double  --> <!-- VAT total value -->
      <brutto>25400.0</brutto>                                      <!-- REQ double  --> <!-- gross total value -->
      <fokonyv>                                                             <!--             --> <!-- general ledger information -->
        <arbevetel>...</arbevetel>                                   <!--     string  --> <!-- sales general ledger ID  -->
        <afa>...</afa>                                                     <!--     string  --> <!-- VAT general ledger ID -->
      </fokonyv>
    </tetel>
    <tetel>
      <megnevezes>Puppy doormat</megnevezes>
      <mennyiseg>2.0</mennyiseg>
      <mennyisegiEgyseg>db</mennyisegiEgyseg>
      <nettoEgysegar>10000</nettoEgysegar>
      <netto>20000.0</netto>
      <afakulcs>ÁKK</afakulcs>
      <afa>5400.0</afa>
      <brutto>25400.0</brutto>
    </tetel>
  </tetelek>
  <!--
    The <kifizetesek> section (payments) is not mandatory, but if present,
    then the sum of the values should be equal with the total amount of the receipt.
  -->
  <kifizetesek>                                                             <!--     string  --> <!-- details of the payment method -->
    <kifizetes>
      <fizetoeszkoz>voucher</fizetoeszkoz>                    <!-- REQ string  --> <!-- name of the legal tender -->
      <osszeg>30000.0</osszeg>                                    <!-- REQ double  --> <!-- paid amount with legal tender -->
      <leiras>OTP SZÉP kártya</leiras>                            <!--     double  --> <!-- description of the legal tender -->
    </kifizetes>
    <kifizetes>
      <fizetoeszkoz>debit card</fizetoeszkoz>
      <osszeg>20800.0</osszeg>
    </kifizetes>
  </kifizetesek>
</xmlnyugtacreate>"""


# language=XML
reverse_receipt = """<?xml version="1.0" encoding="UTF-8"?>
<xmlnyugtast xmlns="http://www.szamlazz.hu/xmlnyugtast"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://www.szamlazz.hu/xmlnyugtast http://www.szamlazz.hu/docs/xsds/nyugtast/xmlnyugtast.xsd">
  <beallitasok>
    <felhasznalo>{{ felhasznalo }}</felhasznalo>
    <jelszo>{{ jelszo }}</jelszo>
    <szamlaagentkulcs>{{ szamlaagentkulcs }}</szamlaagentkulcs>
    <pdfLetoltes>{{ pdfLetoltes }}</pdfLetoltes>
  </beallitasok> 
  <fejlec>
    <nyugtaszam>{{ nyugtaszam }}</nyugtaszam>
    {% if pdfSablon | length %}
    <pdfSablon>{{ pdfSablon }}</pdfSablon>
    {% endif %}
  </fejlec>
</xmlnyugtast>"""

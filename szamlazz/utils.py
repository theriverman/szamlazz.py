__all__ = ["PdfDataMissingError", "template_xml_generate_invoice", ]


class PdfDataMissingError(Exception):
    pass


# language=XML
template_xml_generate_invoice: str = """<?xml version="1.0" encoding="UTF-8"?>
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
template_xml_reverse_invoice = """<?xml version="1.0" encoding="UTF-8"?>
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
        <szamlaSablon>{{ header.invoice_template }}</szamlaSablon>  <!-- Értékkészlet: 'SzlaMost' | 'SzlaAlap' | 'SzlaNoEnv' | 'Szla8cm' | 'SzlaTomb' | 'SzlaFuvarlevelesAlap' -->
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

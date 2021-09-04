from lxml import etree
from typing import Tuple


__all__ = ["validate", ]


class ValidationError(Exception):
    pass


def validate(xml: str, xsd: str) -> Tuple[bool, str]:
    parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
    # XSD
    xmlschema_doc = etree.fromstring(xsd.encode('utf-8'), parser=parser)
    xmlschema = etree.XMLSchema(xmlschema_doc)

    # XML
    xml_doc = etree.fromstring(xml.encode('utf-8'), parser=parser)
    result = xmlschema.validate(xml_doc)

    # xmlschema.error_log.last_error => lxml.etree._LogEntry
    return result, str(xmlschema.error_log.last_error)


# language=XSD
generate_invoice = """<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://www.w3.org/2001/XMLSchema" targetNamespace="http://www.szamlazz.hu/xmlszamla" xmlns:tns="http://www.szamlazz.hu/xmlszamla" elementFormDefault="qualified">

    <complexType name="vevoTipus">
        <sequence>
            <element name="nev" type="string" maxOccurs="1" minOccurs="1"></element>
            <element name="orszag" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="irsz" type="string" maxOccurs="1" minOccurs="1"></element>
            <element name="telepules" type="string" maxOccurs="1" minOccurs="1"></element>
            <element name="cim" type="string" maxOccurs="1" minOccurs="1"></element>
            <element name="email" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="sendEmail" type="boolean" maxOccurs="1" minOccurs="0"></element>
            <element name="adoalany" type="int" maxOccurs="1" minOccurs="0"></element>            <!-- Possible values for the "type" field: 7:business is based outside of the European Union, 6:business is based in the Europen Union, 1: has a hungarian tax number, 0: we don't know, if the buyer has a tax number, -1: no tax number -->
            <element name="adoszam" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="adoszamEU" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="postazasiNev" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="postazasiOrszag" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="postazasiIrsz" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="postazasiTelepules" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="postazasiCim" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="vevoFokonyv" type="tns:vevoFokonyvTipus" maxOccurs="1" minOccurs="0"></element>                        
            <element name="azonosito" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="alairoNeve" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="telefonszam" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="megjegyzes" type="string" maxOccurs="1" minOccurs="0"></element>
        </sequence>
    </complexType>

    <complexType name="vevoFokonyvTipus">
        <sequence>
            <element name="konyvelesDatum" type="date" maxOccurs="1" minOccurs="0"></element>
            <element name="vevoAzonosito" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="vevoFokonyviSzam" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="folyamatosTelj" type="boolean" maxOccurs="1" minOccurs="0"></element>
            <element name="elszDatumTol" type="date" maxOccurs="1" minOccurs="0"></element>
            <element name="elszDatumIg" type="date" maxOccurs="1" minOccurs="0"></element>
        </sequence>
    </complexType>

    <complexType name="eladoTipus">
        <sequence>
            <element name="bank" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="bankszamlaszam" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="emailReplyto" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="emailTargy" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="emailSzoveg" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="alairoNeve" type="string" maxOccurs="1" minOccurs="0"></element>
        </sequence>
    </complexType>

    <complexType name="beallitasokTipus">
        <sequence>
            <element name="felhasznalo" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="jelszo" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="szamlaagentkulcs" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="eszamla" type="boolean" maxOccurs="1" minOccurs="1"></element>
            <element name="szamlaLetoltes" type="boolean" maxOccurs="1" minOccurs="1"></element>
            <element name="szamlaLetoltesPld" type="int" maxOccurs="1" minOccurs="0"></element>
            <element name="valaszVerzio" type="int" maxOccurs="1" minOccurs="0"></element>
            <element name="aggregator" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="guardian" type="boolean" maxOccurs="1" minOccurs="0"></element>
            <element name="cikkazoninvoice" type="boolean" maxOccurs="1" minOccurs="0"></element>

        </sequence>
    </complexType>

    <complexType name="tetelTipus">
        <sequence>
            <element name="megnevezes" type="string" maxOccurs="1" minOccurs="1"></element>
            <element name="azonosito" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="mennyiseg" type="double" maxOccurs="1" minOccurs="1"></element>
            <element name="mennyisegiEgyseg" type="string" maxOccurs="1" minOccurs="1"></element>
            <element name="nettoEgysegar" type="double" maxOccurs="1" minOccurs="1"></element>
            <element name="afakulcs" type="string" maxOccurs="1" minOccurs="1"></element>
            <element name="arresAfaAlap" type="double" maxOccurs="1" minOccurs="0"></element>                        
            <element name="nettoErtek" type="double" maxOccurs="1" minOccurs="1"></element>
            <element name="afaErtek" type="double" maxOccurs="1" minOccurs="1"></element>
            <element name="bruttoErtek" type="double" maxOccurs="1" minOccurs="1"></element>
            <element name="megjegyzes" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="tetelFokonyv" type="tns:tetelFokonyvTipus" maxOccurs="1" minOccurs="0"></element>
        </sequence>
    </complexType>

    <complexType name="tetelekTipus">
        <sequence>
            <element name="tetel" type="tns:tetelTipus" maxOccurs="unbounded" minOccurs="1"></element>
        </sequence>
    </complexType>

    <complexType name="tetelFokonyvTipus">
        <sequence>
            <element name="gazdasagiEsem" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="gazdasagiEsemAfa" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="arbevetelFokonyviSzam" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="afaFokonyviSzam" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="elszDatumTol" type="date" maxOccurs="1" minOccurs="0"></element>
            <element name="elszDatumIg" type="date" maxOccurs="1" minOccurs="0"></element>
        </sequence>
    </complexType>

    <complexType name="fejlecTipus">
        <sequence>
            <element name="keltDatum" type="date" maxOccurs="1" minOccurs="0"></element>
            <element name="teljesitesDatum" type="date" maxOccurs="1" minOccurs="1"></element>
            <element name="fizetesiHataridoDatum" type="date" maxOccurs="1" minOccurs="1"></element>
            <element name="fizmod" type="string" maxOccurs="1" minOccurs="1"></element>
            <element name="penznem" type="string" maxOccurs="1"    minOccurs="1"></element>
            <element name="szamlaNyelve" type="tns:szamlaNyelveTipus" maxOccurs="1" minOccurs="1"></element>
            <element name="megjegyzes" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="arfolyamBank" type="string" maxOccurs="1" minOccurs="0"></element>   
            <element name="arfolyam" type="double" maxOccurs="1" minOccurs="0"></element>            <!-- If arfolyamBank='MNB' AND ther is no exchange rate, then the current exchange rate of MNB  will be used durring receipt creation (automatic MNB exchange rate import) -->
            <element name="rendelesSzam" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="dijbekeroSzamlaszam" type="string" maxOccurs="1" minOccurs="0"></element> <!-- link to prepayment request -->
            <element name="elolegszamla" type="boolean" maxOccurs="1" minOccurs="0"></element>
            <element name="vegszamla" type="boolean" maxOccurs="1" minOccurs="0"></element>
            <element name="helyesbitoszamla" type="boolean" maxOccurs="1" minOccurs="0"></element>
            <element name="helyesbitettSzamlaszam" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="dijbekero" type="boolean" maxOccurs="1" minOccurs="0"></element>
            <element name="szallitolevel" type="boolean" maxOccurs="1" minOccurs="0"></element>
            <element name="logoExtra" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="szamlaszamElotag" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="fizetendoKorrekcio" type="double" maxOccurs="1" minOccurs="0"></element>
            <element name="fizetve" type="boolean" maxOccurs="1" minOccurs="0"></element>
            <element name="arresAfa" type="boolean" maxOccurs="1" minOccurs="0"></element>
            <element name="eusAfa" type="boolean" maxOccurs="1" minOccurs="0"></element>            <!-- There is no hungarian VAT on the receipt. Data disclosure towards NTCAs Online Invoice System is not needed. -->
            <element name="szamlaSablon" type="string" maxOccurs="1" minOccurs="0"></element>       <!-- Codomain: 'SzlaMost' | 'SzlaAlap' | 'SzlaNoEnv' | 'Szla8cm' | 'SzlaTomb' | 'szlafuvarlevelesalap'-->
            <element name="elonezetpdf" type="boolean" maxOccurs="1" minOccurs="0"></element>       <!-- warrant preview pdf (no warrant is created) --> 
        </sequence>
    </complexType>

    <simpleType name="szamlaNyelveTipus">
        <restriction base="string">
            <enumeration value="hu"></enumeration>
            <enumeration value="en"></enumeration>
            <enumeration value="de"></enumeration>
            <enumeration value="it"></enumeration>
            <enumeration value="ro"></enumeration>
            <enumeration value="sk"></enumeration>
            <enumeration value="hr"></enumeration>
            <enumeration value="fr"></enumeration>
            <enumeration value="es"></enumeration>
            <enumeration value="cz"></enumeration>
            <enumeration value="pl"></enumeration>
        </restriction>
    </simpleType>

    <complexType name="transoflexTipus">
        <sequence>
            <!-- 5 digit number provided by TOF -->
            <element name="azonosito" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="shipmentID" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="csomagszam" type="int" maxOccurs="1" minOccurs="0"></element>
            <element name="countryCode" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="zip" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="service" type="string" maxOccurs="1" minOccurs="0"></element>
        </sequence>
    </complexType>

    <complexType name="sprinterTipus">
        <sequence>
            <!-- 3-character abbreviation agreed with Sprinter -->
            <element name="azonosito" type="string" maxOccurs="1" minOccurs="0"></element>
            <!-- 10-character long "feladókód" provided by Sprinter -->
            <element name="feladokod" type="string" maxOccurs="1" minOccurs="0"></element>
            <!-- "Iránykód" from Sprinter is Sprinters own special parcel shipment code, eg. "106" -->
            <element name="iranykod" type="string" maxOccurs="1" minOccurs="0"></element>
            <!--    Number of packages, this shows how many consignment note will be attached to the receipt-->
            <element name="csomagszam" type="int" maxOccurs="1" minOccurs="0"></element>
            <!-- unique per receipt, 7-13 characters long identifyer -->
            <element name="vonalkodPostfix" type="string" maxOccurs="1" minOccurs="0"></element>
            <!-- usually this is the 1 work day note -->
            <element name="szallitasiIdo" type="string" maxOccurs="1" minOccurs="0"></element>
        </sequence>
    </complexType>

    <complexType name="pppTipus">
        <sequence>
            <!-- 3-character abbreviation agreed with PPP -->
            <element name="vonalkodPrefix" type="string" maxOccurs="1" minOccurs="0"></element>
            <!-- unique per receipt, MAX 7 characters long identifyer -->
            <element name="vonalkodPostfix" type="string" maxOccurs="1" minOccurs="0"></element>
        </sequence>
    </complexType>

    <complexType name="mplTipus">
        <sequence>
            <!-- MPL customer code -->
            <element name="vevokod" type="string" maxOccurs="1" minOccurs="1"></element>
            <!-- Bar code is generated based on thes string -->
            <element name="vonalkod" type="string" maxOccurs="1" minOccurs="1"></element>
            <!-- Weight of the package, can contain a decimal point, if necessary -->
            <element name="tomeg" type="string" maxOccurs="1" minOccurs="1"></element>
            <!-- Optional configuration for special services icons, if not defined no icon will be shown -->
            <element name="kulonszolgaltatasok" type="string" maxOccurs="1" minOccurs="0"></element>
            <!--    Vallue ("erteknyilvanitas") field on the consignment note -->
            <element name="erteknyilvanitas" type="double" maxOccurs="1" minOccurs="0"></element>
        </sequence>
    </complexType>

    <complexType name="fuvarlevelTipus">
        <sequence>
            <!-- TODO   the destination ("uticel") field is not used, should be removed after 2014.05.30, sprinter/iranykod field should be used instead  -->
            <element name="uticel" type="string" maxOccurs="1" minOccurs="0"></element>
            <!-- Codomain: TOF, PPP, SPRINTER, FOXPOST, EMPTY ,not necessary if there is no consignment note -->
            <element name="futarSzolgalat" type="string" maxOccurs="1" minOccurs="0"></element>
            <!--General bar code definition, this will be used, if no carrierspecific data is defined -->
            <element name="vonalkod" type="string" maxOccurs="1" minOccurs="0"></element>
            <!-- Comment on the consignment note -->
            <element name="megjegyzes" type="string" maxOccurs="1" minOccurs="0"></element>
            <!-- Trans-O-Flex node to upload -->
            <element name="tof" type="tns:transoflexTipus" maxOccurs="1" minOccurs="0"></element>
            <!-- PickPackPoint node to upload -->
            <element name="ppp" type="tns:pppTipus" maxOccurs="1" minOccurs="0"></element>
            <!-- Sprinter node to upload -->
            <element name="sprinter" type="tns:sprinterTipus" maxOccurs="1" minOccurs="0"></element>
            <!-- MPL node to upload-->
            <element name="mpl" type="tns:mplTipus" maxOccurs="1" minOccurs="0"></element>
        </sequence>
    </complexType>

    <element name="xmlszamla">
        <complexType>
            <sequence>
                <element name="beallitasok" type="tns:beallitasokTipus" maxOccurs="1" minOccurs="1"></element>
                <element name="fejlec" type="tns:fejlecTipus" maxOccurs="1" minOccurs="1"></element>
                <element name="elado" type="tns:eladoTipus" maxOccurs="1" minOccurs="1"></element>
                <element name="vevo" type="tns:vevoTipus" maxOccurs="1" minOccurs="1"></element>
                <element name="fuvarlevel" type="tns:fuvarlevelTipus" maxOccurs="1" minOccurs="0"></element>
                <element name="tetelek" type="tns:tetelekTipus" maxOccurs="1" minOccurs="1"></element>
            </sequence>
        </complexType>
    </element>
</schema>
"""

# language=XSD
reverse_invoice = """<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://www.w3.org/2001/XMLSchema" targetNamespace="http://www.szamlazz.hu/xmlszamlast" xmlns:tns="http://www.szamlazz.hu/xmlszamlast" elementFormDefault="qualified">
    <complexType name="vevoTipus"><!-- If the TAX number of the buyer is missing from the original invoice, it can be added in this block -->
        <sequence>
            <element name="email" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="adoszam"   type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="adoszamEU" type="string" maxOccurs="1" minOccurs="0"></element>
        </sequence>
    </complexType>
    <complexType name="eladoTipus">
        <sequence>
            <element name="emailReplyto" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="emailTargy" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="emailSzoveg" type="string" maxOccurs="1" minOccurs="0"></element>
        </sequence>
    </complexType>
    <complexType name="beallitasokTipus">
        <sequence>
            <element name="felhasznalo" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="jelszo" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="szamlaagentkulcs" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="eszamla" type="boolean" maxOccurs="1" minOccurs="1"></element>
            <element name="szamlaLetoltes" type="boolean" maxOccurs="1" minOccurs="1"></element>
            <element name="szamlaLetoltesPld" type="int" maxOccurs="1" minOccurs="0"></element>
            <element name="aggregator" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="guardian" type="boolean" maxOccurs="1" minOccurs="0"></element>
            <element name="valaszVerzio" type="int" maxOccurs="1" minOccurs="0"></element>
        </sequence>
    </complexType>
    <complexType name="fejlecTipus">
        <sequence>
            <element name="szamlaszam"      type="string" maxOccurs="1" minOccurs="1"></element>
            <element name="keltDatum"       type="date"   maxOccurs="1" minOccurs="0"></element>
            <element name="teljesitesDatum" type="date"   maxOccurs="1" minOccurs="0"></element>
            <element name="tipus"           type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="szamlaSablon"    type="string" maxOccurs="1" minOccurs="0"></element> <!-- Értékkészlet: 'SzlaMost' | 'SzlaAlap' | 'SzlaNoEnv' | 'Szla8cm' | 'SzlaTomb' | 'SzlaFuvarlevelesAlap' -->
        </sequence>
    </complexType>

    <element name="xmlszamlast">
        <complexType>
            <sequence>
                <element name="beallitasok" type="tns:beallitasokTipus" maxOccurs="1" minOccurs="1"></element>
                <element name="fejlec" type="tns:fejlecTipus" maxOccurs="1" minOccurs="1"></element>
                <element name="elado" type="tns:eladoTipus" maxOccurs="1" minOccurs="0"></element>
                <element name="vevo" type="tns:vevoTipus" maxOccurs="1" minOccurs="0"></element>
            </sequence>
        </complexType>
    </element>
</schema>
"""

# language=XSD
credit_entry = """<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://www.w3.org/2001/XMLSchema" targetNamespace="http://www.szamlazz.hu/xmlszamlakifiz" xmlns:tns="http://www.szamlazz.hu/xmlszamlakifiz" elementFormDefault="qualified">
<complexType name="beallitasokTipus">
  <sequence>
    <element name="felhasznalo" type="string" maxOccurs="1" minOccurs="0"></element>
    <element name="jelszo" type="string" maxOccurs="1" minOccurs="0"></element>
    <element name="szamlaagentkulcs" type="string" maxOccurs="1" minOccurs="0"></element>
    <element name="szamlaszam" type="string" maxOccurs="1" minOccurs="1"></element>
    <element name="additiv" type="boolean" maxOccurs="1" minOccurs="1"></element>
  </sequence>
</complexType>
<complexType name="kifizetesTipus">
  <sequence>
    <element name="datum" type="date" maxOccurs="1" minOccurs="1"></element>
    <element name="jogcim" type="string" maxOccurs="1" minOccurs="1"></element>
    <element name="osszeg" type="double" maxOccurs="1" minOccurs="1"></element>
    <element name="leiras" type="string" maxOccurs="1" minOccurs="0"></element>
  </sequence>
</complexType>
<complexType name="szamlaKifizTipus">
  <sequence>
    <element name="beallitasok" type="tns:beallitasokTipus" maxOccurs="1" minOccurs="1"></element>
    <element name="kifizetes" type="tns:kifizetesTipus" maxOccurs="5" minOccurs="0"></element>
  </sequence>
</complexType>
<element name="xmlszamlakifiz" type="tns:szamlaKifizTipus"></element>
</schema>"""


# language=XSD
query_invoice_pdf = """<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://www.w3.org/2001/XMLSchema" targetNamespace="http://www.szamlazz.hu/xmlszamlapdf"
xmlns:tns="http://www.szamlazz.hu/xmlszamlapdf" elementFormDefault="qualified">
  <complexType name="beallitasokTipus">
    <sequence>
      <element name="felhasznalo" type="string" maxOccurs="1" minOccurs="0"></element>
      <element name="jelszo" type="string" maxOccurs="1" minOccurs="0"></element>
      <element name="szamlaagentkulcs" type="string" maxOccurs="1" minOccurs="0"></element>      
      <element name="szamlaszam" type="string" maxOccurs="1" minOccurs="1"></element>
      <element name="valaszVerzio" type="int" maxOccurs="1" minOccurs="1"></element>
    </sequence>
  </complexType>
  <element name="xmlszamlapdf" type="tns:beallitasokTipus"></element>
</schema>
"""


# language=XSD
query_invoice_xml = """<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://www.w3.org/2001/XMLSchema" targetNamespace="http://www.szamlazz.hu/xmlszamlaxml" xmlns:tns="http://www.szamlazz.hu/xmlszamlaxml" elementFormDefault="qualified">
    <element name="xmlszamlaxml">
        <complexType>
            <sequence>
                <element name="felhasznalo" type="string" maxOccurs="1" minOccurs="0"></element>
                <element name="jelszo" type="string" maxOccurs="1" minOccurs="0"></element>
                <element name="szamlaagentkulcs" type="string" maxOccurs="1" minOccurs="0"></element>
                <element name="szamlaszam" type="string" maxOccurs="1" minOccurs="0"></element>
                <element name="rendelesSzam" type="string" maxOccurs="1" minOccurs="0"></element>
                <element name="pdf" type="boolean" maxOccurs="1" minOccurs="0"></element>
            </sequence>
        </complexType>
    </element>
</schema>"""


# language=XML
delete_pro_forma_invoice = """<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://www.w3.org/2001/XMLSchema" targetNamespace="http://www.szamlazz.hu/xmlszamladbkdel" xmlns:tns="http://www.szamlazz.hu/xmlszamladbkdel" elementFormDefault="qualified">
    <complexType name="beallitasokTipus">
        <sequence>
            <element name="felhasznalo" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="jelszo" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="szamlaagentkulcs" type="string" maxOccurs="1" minOccurs="0"></element>
        </sequence>
    </complexType>
    <complexType name="fejlecTipus">
        <sequence>
            <element name="szamlaszam" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="rendelesszam" type="string" maxOccurs="1" minOccurs="0"></element>
        </sequence>
    </complexType>
    <element name="xmlszamladbkdel">
      <complexType>
     <sequence>
        <element name="beallitasok" type="tns:beallitasokTipus" maxOccurs="1" minOccurs="1"></element>
        <element name="fejlec" type="tns:fejlecTipus" maxOccurs="1" minOccurs="1"></element>
     </sequence>
      </complexType>
    </element>
</schema>"""


# language=XML
generate_receipt = """<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://www.w3.org/2001/XMLSchema" targetNamespace="http://www.szamlazz.hu/xmlnyugtacreate" xmlns:tns="http://www.szamlazz.hu/xmlnyugtacreate" elementFormDefault="qualified">
    <complexType name="beallitasokTipus">
        <all>
            <element name="felhasznalo" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="jelszo" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="szamlaagentkulcs" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="pdfLetoltes" type="boolean" maxOccurs="1" minOccurs="1"></element>
        </all>
    </complexType>
    <complexType name="fejlecTipus">
        <all>
            <element name="hivasAzonosito" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="elotag" type="string" maxOccurs="1" minOccurs="1"></element>
            <element name="fizmod" type="string" maxOccurs="1" minOccurs="1"></element>
            <element name="penznem" type="string" maxOccurs="1" minOccurs="1"></element>
            <element name="devizaarf" type="double" maxOccurs="1" minOccurs="0"></element>
            <element name="devizabank" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="megjegyzes" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="pdfSablon" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="fokonyvVevo" type="string" maxOccurs="1" minOccurs="0"></element>
        </all>
    </complexType>
    <complexType name="tetelTipus">
        <all>
            <element name="megnevezes" type="string" maxOccurs="1" minOccurs="1"></element>
            <element name="azonosito" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="mennyiseg" type="double" maxOccurs="1" minOccurs="1"></element>
            <element name="mennyisegiEgyseg" type="string" maxOccurs="1" minOccurs="1"></element>
            <element name="nettoEgysegar" type="double" maxOccurs="1" minOccurs="1"></element>
            <element name="afakulcs" type="string" maxOccurs="1" minOccurs="1"></element>
            <element name="netto" type="double" maxOccurs="1" minOccurs="1"></element>
            <element name="afa" type="double" maxOccurs="1" minOccurs="1"></element>
            <element name="brutto" type="double" maxOccurs="1" minOccurs="1"></element>
            <element name="fokonyv" type="tns:tetelFokonyvTipus" maxOccurs="1" minOccurs="0"></element>
        </all>
    </complexType>
    <complexType name="tetelFokonyvTipus">
        <all>
            <element name="arbevetel" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="afa" type="string" maxOccurs="1" minOccurs="0"></element>
        </all>
    </complexType>
    <complexType name="tetelekTipus">
        <sequence>
            <element name="tetel" type="tns:tetelTipus" maxOccurs="unbounded" minOccurs="1"></element>
        </sequence>
    </complexType>
    <!-- jóváírások -->
    <complexType name="kifizetesTipus">
        <all>
            <element name="fizetoeszkoz" type="string" maxOccurs="1" minOccurs="1"></element>
            <element name="osszeg" type="double" maxOccurs="1" minOccurs="1"></element>
            <element name="leiras" type="string" maxOccurs="1" minOccurs="0"></element>
        </all>
    </complexType>
    <complexType name="kifizetesekTipus">
        <sequence>
            <element name="kifizetes"             type="tns:kifizetesTipus"   maxOccurs="unbounded" minOccurs="1"></element>
        </sequence>
    </complexType>
    <element name="xmlnyugtacreate">
        <complexType>
            <all>
                <element name="beallitasok" type="tns:beallitasokTipus" maxOccurs="1" minOccurs="1"></element>
                <element name="fejlec" type="tns:fejlecTipus" maxOccurs="1" minOccurs="1"></element>
                <element name="tetelek" type="tns:tetelekTipus" maxOccurs="1" minOccurs="1"></element>
                <element name="kifizetesek" type="tns:kifizetesekTipus" maxOccurs="1" minOccurs="0"></element>
            </all>
        </complexType>
    </element>
</schema>"""


# language=XML
reverse_receipt = """<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://www.w3.org/2001/XMLSchema" targetNamespace="http://www.szamlazz.hu/xmlnyugtast" xmlns:tns="http://www.szamlazz.hu/xmlnyugtast" elementFormDefault="qualified">
    <complexType name="beallitasokTipus">
        <sequence>
            <element name="felhasznalo" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="jelszo" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="szamlaagentkulcs" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="pdfLetoltes" type="boolean" maxOccurs="1" minOccurs="1"></element>
        </sequence>
    </complexType>
    <complexType name="fejlecTipus">
        <sequence>
            <element name="nyugtaszam" type="string" maxOccurs="1" minOccurs="1"></element>
            <element name="pdfSablon" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="hivasAzonosito" type="string" maxOccurs="1" minOccurs="0"></element>
        </sequence>
    </complexType>
    <element name="xmlnyugtast">
        <complexType>
            <sequence>
                <element name="beallitasok" type="tns:beallitasokTipus" maxOccurs="1" minOccurs="1"></element>
                <element name="fejlec" type="tns:fejlecTipus" maxOccurs="1" minOccurs="1"></element>
            </sequence>
        </complexType>
    </element>
</schema>"""


# language=XML
query_receipt = """<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://www.w3.org/2001/XMLSchema" targetNamespace="http://www.szamlazz.hu/xmlnyugtaget" xmlns:tns="http://www.szamlazz.hu/xmlnyugtaget" elementFormDefault="qualified">
    <complexType name="beallitasokTipus">
        <all>
            <element name="felhasznalo" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="jelszo" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="szamlaagentkulcs" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="pdfLetoltes" type="boolean" maxOccurs="1" minOccurs="1"></element>
        </all>
    </complexType>
    <complexType name="fejlecTipus">
        <all>
            <element name="nyugtaszam" type="string" maxOccurs="1" minOccurs="1"></element>
            <element name="hivasAzonosito" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="pdfSablon" type="string" maxOccurs="1" minOccurs="0"></element>
        </all>
    </complexType>
    <element name="xmlnyugtaget">
        <complexType>
            <all>
                <element name="beallitasok" type="tns:beallitasokTipus" maxOccurs="1" minOccurs="1"></element>
                <element name="fejlec" type="tns:fejlecTipus" maxOccurs="1" minOccurs="1"></element>
            </all>
        </complexType>
    </element>
</schema>"""


# language=XML
send_receipt = """<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://www.w3.org/2001/XMLSchema" targetNamespace="http://www.szamlazz.hu/xmlnyugtasend" xmlns:tns="http://www.szamlazz.hu/xmlnyugtasend" elementFormDefault="qualified">
    <complexType name="beallitasokTipus">
        <sequence>
            <element name="felhasznalo" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="jelszo" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="szamlaagentkulcs" type="string" maxOccurs="1" minOccurs="0"></element>
        </sequence>
    </complexType>
    <complexType name="fejlecTipus">
        <sequence>
            <element name="nyugtaszam" type="string" maxOccurs="1" minOccurs="1"></element>
        </sequence>
    </complexType>
    <complexType name="emailKuldes">
        <sequence>
            <element name="email" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="emailReplyto" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="emailTargy" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="emailSzoveg" type="string" maxOccurs="1" minOccurs="0"></element>
        </sequence>
    </complexType>
    <element name="xmlnyugtasend">
        <complexType>
            <sequence>
                <element name="beallitasok" type="tns:beallitasokTipus" maxOccurs="1" minOccurs="1"></element>
                <element name="fejlec" type="tns:fejlecTipus" maxOccurs="1" minOccurs="1"></element>
                <element name="emailKuldes" type="tns:emailKuldes" maxOccurs="1" minOccurs="0"></element>
            </sequence>
        </complexType>
    </element>
</schema>"""


# language=XML
tax_payer = """<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://www.w3.org/2001/XMLSchema" targetNamespace="http://www.szamlazz.hu/xmltaxpayer" xmlns:tns="http://www.szamlazz.hu/xmltaxpayer" elementFormDefault="qualified">
    <complexType name="beallitasokTipus">
        <sequence>
            <element name="felhasznalo" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="jelszo" type="string" maxOccurs="1" minOccurs="0"></element>
            <element name="szamlaagentkulcs" type="string" maxOccurs="1" minOccurs="0"></element>
        </sequence>
    </complexType>
    <simpleType name="torszszamTipus">
        <restriction base="string">
            <length value="8" />
            <pattern value="[0-9]{8}" />
        </restriction>
    </simpleType>
    <element name="xmltaxpayer">
        <complexType>
            <sequence>
                <element name="beallitasok" type="tns:beallitasokTipus"maxOccurs="1" minOccurs="1"></element>
                <element name="torzsszam" type="tns:torszszamTipus"maxOccurs="1" minOccurs="1"></element>
            </sequence>
        </complexType>
    </element>
</schema>"""

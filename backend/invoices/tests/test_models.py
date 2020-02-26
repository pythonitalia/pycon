import pytest
from invoices.models import Address, Invoice
from lxml import etree


def _xml_to_string(xml):
    return etree.tostring(xml, pretty_print=True).decode("utf-8")


@pytest.mark.xfail
def test_xml_generation(sample_invoice_xml):
    invoice = Invoice()

    invoice_xml = _xml_to_string(invoice.to_xml())
    sample_xml = _xml_to_string(sample_invoice_xml)

    assert invoice_xml == sample_xml


@pytest.mark.django_db
def test_xml_header_generation(sample_invoice):
    xml = sample_invoice.to_xml()

    assert xml is not None

    header = xml.xpath(
        "/p:FatturaElettronica/FatturaElettronicaHeader",
        namespaces={
            "p": "http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2"
        },
    )[0]

    t_data = header.xpath("DatiTrasmissione")[0]

    assert t_data.xpath("IdTrasmittente/IdPaese")[0].text == "IT"
    assert t_data.xpath("IdTrasmittente/IdCodice")[0].text == "PIABCDE"
    assert t_data.xpath("ProgressivoInvio")[0].text == "1"
    assert t_data.xpath("FormatoTrasmissione")[0].text == "FPR12"
    assert t_data.xpath("CodiceDestinatario")[0].text == "ABCDEFG"
    assert len(t_data.xpath("PecDestinatario")) == 0

    # TODO: might need to add this to the invoice, in order to be able to
    # TODO: use different party for invoices (if ever needed)

    # Supplier data

    s_data = header.xpath("CedentePrestatore/DatiAnagrafici")[0]

    assert s_data.xpath("IdFiscaleIVA/IdPaese")[0].text == "IT"

    # TODO: add this to the model if it is the P. IVA
    # assert s_data.xpath("IdFiscaleIVA/IdCodice")[0].text == "IT"

    assert s_data.xpath("RegimeFiscale")[0].text == "RF01"
    assert s_data.xpath("Anagrafica/Denominazione")[0].text == "Python Italia APS"

    a_data = header.xpath("CedentePrestatore/Sede")[0]

    assert a_data.xpath("Indirizzo")[0].text == "Via Mugellese 1/A"
    assert a_data.xpath("CAP")[0].text == "50013"
    assert a_data.xpath("Comune")[0].text == "Campi Bisenzio"
    assert a_data.xpath("Provincia")[0].text == "FI"
    assert a_data.xpath("Nazione")[0].text == "IT"

    # Client data

    c_data = header.xpath("CessionarioCommittente/DatiAnagrafici")[0]

    assert c_data.xpath("IdFiscaleIVA/IdPaese")[0].text == "IT"
    # TODO: this should be vat code
    assert c_data.xpath("IdFiscaleIVA/IdCodice")[0].text == "aaabbb12b34z123d"
    # assert c_data.xpath("Anagrafica/Nome")[0].text == "Patrick"
    # assert c_data.xpath("Anagrafica/Cognome")[0].text == "A"

    ca_data = header.xpath("CessionarioCommittente/Sede")[0]

    assert ca_data.xpath("Indirizzo")[0].text == "Via Roma 1"
    assert ca_data.xpath("CAP")[0].text == "83100"
    assert ca_data.xpath("Comune")[0].text == "Avellino"
    assert ca_data.xpath("Provincia")[0].text == "AV"
    assert ca_data.xpath("Nazione")[0].text == "IT"


@pytest.mark.django_db
def test_xml_header_generation_with_pec(sample_invoice):
    sample_invoice.recipient_code = ""
    sample_invoice.recipient_pec = "patrick@python.it"

    xml = sample_invoice.to_xml()

    header = xml.xpath(
        "/p:FatturaElettronica/FatturaElettronicaHeader",
        namespaces={
            "p": "http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2"
        },
    )[0]

    t_data = header.xpath("DatiTrasmissione")[0]

    assert t_data.xpath("CodiceDestinatario")[0].text == "0000000"
    assert t_data.xpath("PecDestinatario")[0].text == "patrick@python.it"


@pytest.mark.django_db
def test_xml_body_generation(sample_invoice):
    xml = sample_invoice.to_xml()

    assert xml is not None

    body = xml.xpath(
        "/p:FatturaElettronica/FatturaElettronicaBody",
        namespaces={
            "p": "http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2"
        },
    )[0]

    general_data = body.xpath("DatiGenerali/DatiGeneraliDocumento")[0]

    assert general_data.xpath("TipoDocumento")[0].text == "TD01"
    assert general_data.xpath("Data")[0].text == "2019-06-16"
    assert general_data.xpath("Divisa")[0].text == "EUR"
    assert general_data.xpath("Numero")[0].text == "00001A"

    # make sure the limit for the causal is respected (200 chars)
    assert len(general_data.xpath("Causale")) == 2
    assert general_data.xpath("Causale")[0].text == "A" * 200
    assert general_data.xpath("Causale")[1].text == "B" * 200

    # Invoice summary

    summary = body.xpath("DatiBeniServizi")[0]

    assert len(summary.xpath("DettaglioLinee")) == 2

    first_item = summary.xpath("DettaglioLinee")[0]
    second_item = summary.xpath("DettaglioLinee")[1]

    assert first_item.xpath("NumeroLinea")[0].text == "1"
    assert first_item.xpath("Descrizione")[0].text == "item 1"
    assert first_item.xpath("Quantita")[0].text == "1.00"
    assert first_item.xpath("PrezzoUnitario")[0].text == "1.00"
    assert first_item.xpath("PrezzoTotale")[0].text == "1.00"
    assert first_item.xpath("AliquotaIVA")[0].text == "0.00"

    assert second_item.xpath("NumeroLinea")[0].text == "2"
    assert second_item.xpath("Descrizione")[0].text == "item 2"
    assert second_item.xpath("Quantita")[0].text == "2.00"
    assert second_item.xpath("PrezzoUnitario")[0].text == "2.00"
    assert second_item.xpath("PrezzoTotale")[0].text == "4.00"
    assert second_item.xpath("AliquotaIVA")[0].text == "0.00"

    assert summary.xpath("DatiRiepilogo/AliquotaIVA")[0].text == "22.00"
    assert summary.xpath("DatiRiepilogo/ImponibileImporto")[0].text == "5.00"
    assert summary.xpath("DatiRiepilogo/Imposta")[0].text == "1.10"

    # Payment data

    assert body.xpath("DatiPagamento/CondizioniPagamento")[0].text == "TP02"

    # payment details

    details = body.xpath("DatiPagamento/DettaglioPagamento")[0]

    assert details.xpath("ModalitaPagamento")[0].text == "MP08"
    assert details.xpath("ImportoPagamento")[0].text == "2.00"


def test_address_string():
    ad1 = Address(
        address="Via dei matti, 0",
        postcode="12345",
        city="Agrigento",
        province="AG",
        country_code="IT",
    )
    ad2 = Address(address="Via Dante Alighieri, 4", country_code="IT")
    ad3 = Address(
        address="Via Roma, 9", city="Treviglio", province="BG", country_code="IT"
    )

    assert str(ad1) == "Via dei matti, 0 Agrigento (AG) [IT]"
    assert str(ad2) == "Via Dante Alighieri, 4 [IT]"
    assert str(ad3) == "Via Roma, 9 Treviglio (BG) [IT]"


@pytest.mark.django_db
def test_invoice_string(sample_invoice):
    assert str(sample_invoice) == "[Fattura/00001A] Patrick A: " + (
        "A" * 200 + "B" * 200
    )
    assert sample_invoice.get_filename() == "00001A.xml"


@pytest.mark.django_db
def test_sender_string(sender):
    assert str(sender) == "Python Italia APS"


@pytest.mark.django_db
@pytest.mark.xfail(reason="Needs to be updated")
def test_xml_encoding(sample_invoice):
    sample_invoice.recipient_first_name = "Łukasz"
    sample_invoice.save()

    xml = sample_invoice.to_xml()

    header = xml.xpath(
        "/p:FatturaElettronica/FatturaElettronicaHeader",
        namespaces={
            "p": "http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2"
        },
    )[0]

    name = header.xpath("CessionarioCommittente/DatiAnagrafici/Anagrafica/Nome")[0]

    assert name.text == "Lukasz"

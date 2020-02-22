from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, List

from lxml import etree

from .types import ProductSummary, XMLDict
from .utils import dict_to_xml, format_price

if TYPE_CHECKING:  # pragma: no cover
    from invoices.models import Invoice, Sender, Address


NAMESPACE_MAP = {
    "p": "http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2",
    "ds": "http://www.w3.org/2000/09/xmldsig#",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}

SCHEMA_LOCATION = (
    "http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2 "
    "http://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.2"
    "/Schema_del_file_xml_FatturaPA_versione_1.2.xsd"
)


def _get_recipient_code(invoice: Invoice) -> str:
    if not invoice.recipient_code:
        return "0000000"

    return invoice.recipient_code


def _generate_header(invoice: Invoice) -> XMLDict:
    sender: Sender = invoice.sender
    address: Address = sender.address
    client_address: Address = invoice.recipient_address

    recipient_data = {
        "IdFiscaleIVA": {
            "IdPaese": invoice.recipient_address.country_code,
            "IdCodice": invoice.recipient_tax_code,
        }
    }

    if invoice.recipient_denomination:  # pragma: no cover
        recipient_data["Anagrafica"] = {"Denominazione": invoice.recipient_denomination}
    else:
        recipient_data["Anagrafica"] = {
            "Nome": invoice.recipient_first_name,
            "Cognome": invoice.recipient_last_name or "Mancante",
        }

    header: XMLDict = {
        "FatturaElettronicaHeader": {
            "DatiTrasmissione": {
                "IdTrasmittente": {
                    "IdPaese": sender.country_code,
                    "IdCodice": sender.code,
                },
                "ProgressivoInvio": 1,
                "FormatoTrasmissione": invoice.transmission_format,
                "CodiceDestinatario": _get_recipient_code(invoice),
                "PecDestinatario": invoice.recipient_pec,
            },
            "CedentePrestatore": {
                "DatiAnagrafici": {
                    "IdFiscaleIVA": {
                        "IdPaese": sender.country_code,
                        "IdCodice": sender.code,
                    },
                    "Anagrafica": {"Denominazione": sender.company_name},
                    "RegimeFiscale": sender.tax_regime,
                },
                "Sede": {
                    "Indirizzo": address.address,
                    "CAP": address.postcode,
                    "Comune": address.city,
                    "Provincia": address.province,
                    "Nazione": address.country_code,
                },
            },
            "CessionarioCommittente": {
                "DatiAnagrafici": {**recipient_data},
                "Sede": {
                    "Indirizzo": client_address.address[:60],
                    "CAP": (
                        "00000"
                        if client_address.country_code.lower() != "it"
                        else client_address.postcode
                    ),
                    "Comune": client_address.city,
                    "Provincia": client_address.province,
                    "Nazione": client_address.country_code,
                },
            },
        }
    }

    return header


def _generate_body(invoice: Invoice) -> XMLDict:
    summary: List[ProductSummary] = invoice.invoice_summary
    invoice_amount_without_tax = sum(x["total_price"] for x in summary)
    tax = Decimal(invoice.invoice_tax_rate) * invoice_amount_without_tax / 100

    body: XMLDict = {
        "FatturaElettronicaBody": {
            "DatiGenerali": {
                "DatiGeneraliDocumento": {
                    "TipoDocumento": invoice.invoice_type,
                    "Divisa": invoice.invoice_currency,
                    "Data": invoice.invoice_date.strftime("%Y-%m-%d"),
                    "Numero": invoice.invoice_number,
                    "Causale": invoice.causal,
                }
            },
            "DatiBeniServizi": {
                "DettaglioLinee": [
                    {
                        "NumeroLinea": x["row"],
                        "Descrizione": x["description"],
                        "Quantita": format_price(x["quantity"]),
                        "PrezzoUnitario": format_price(x["unit_price"]),
                        "PrezzoTotale": format_price(x["total_price"]),
                        "AliquotaIVA": format_price(x["vat_rate"]),
                    }
                    for x in summary
                ],
                "DatiRiepilogo": {
                    "AliquotaIVA": format_price(invoice.invoice_tax_rate),
                    "ImponibileImporto": format_price(invoice_amount_without_tax),
                    "Imposta": format_price(tax),
                },
            },
            "DatiPagamento": {
                "CondizioniPagamento": invoice.payment_condition,
                "DettaglioPagamento": {
                    "ModalitaPagamento": invoice.payment_method,
                    "ImportoPagamento": format_price(invoice.invoice_amount),
                },
            },
        }
    }

    return body


def invoice_to_xml(invoice: Invoice) -> etree._Element:
    root_tag = "{%s}FatturaElettronica" % NAMESPACE_MAP["p"]
    schema_location_key = "{%s}schemaLocation" % NAMESPACE_MAP["xsi"]

    root = etree.Element(
        root_tag,
        attrib={schema_location_key: SCHEMA_LOCATION},
        nsmap=NAMESPACE_MAP,
        versione="FPR12",
    )

    header = _generate_header(invoice)
    body = _generate_body(invoice)

    tags = [*dict_to_xml(header), *dict_to_xml(body)]

    for tag in tags:
        root.append(tag)

    return root

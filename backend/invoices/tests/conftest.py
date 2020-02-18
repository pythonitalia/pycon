import os
from datetime import date
from typing import List

import pytest
from invoices.models import Address, Invoice, Item, Sender
from invoices.xml.types import ProductSummary
from lxml import etree


@pytest.fixture
def sample_invoice_xml():
    here = os.path.dirname(__file__)

    parser = etree.XMLParser(remove_blank_text=True)

    root = etree.parse(
        os.path.join(here, "../data/IT01234567890_FPA01.xml"), parser=parser
    )

    for elem in root.iter("*"):
        if elem.text is not None:
            elem.text = elem.text.strip()

    return root


@pytest.fixture
def supplier_address():
    return Address.objects.create(
        address="Via Mugellese 1/A",
        city="Campi Bisenzio",
        postcode="50013",
        province="FI",
        country_code="IT",
    )


@pytest.fixture
def client_address():
    return Address.objects.create(
        address="Via Roma 1",
        city="Avellino",
        postcode="83100",
        province="AV",
        country_code="IT",
    )


@pytest.fixture
def sender(supplier_address):
    return Sender.objects.create(
        name="Python Italia APS",
        code="PIABCDE",
        country_code="IT",
        contact_phone="+390123456789",
        contact_email="info@python.it",
        company_name="Python Italia APS",
        tax_regime="RF01",
        address=supplier_address,
    )


@pytest.fixture
def sample_items() -> List[ProductSummary]:
    return [
        Item(row=1, description="item 1", quantity=1, unit_price=1.0, vat_rate=0),
        Item(row=2, description="item 2", quantity=2, unit_price=2, vat_rate=0),
    ]


@pytest.fixture
def sample_invoice(sender, sample_items, client_address) -> Invoice:
    invoice = Invoice(
        sender=sender,
        invoice_number="00001A",
        invoice_type="TD01",
        invoice_currency="EUR",
        invoice_date=date(2019, 6, 16),
        invoice_deadline=date(2019, 5, 2),
        invoice_tax_rate=22.00,
        invoice_amount=2.00,
        invoice_tax_amount=2.00,
        causal=("A" * 200 + "B" * 200),
        transmission_format="FPR12",
        payment_condition="TP02",
        payment_method="MP08",
        recipient_code="ABCDEFG",
        recipient_tax_code="AAABBB12B34Z123D",
        recipient_first_name="Patrick",
        recipient_last_name="A",
        recipient_address=client_address,
    )
    invoice.save()
    for item in sample_items:
        item.save()
        invoice.items.add(item)
    invoice.save()
    return invoice

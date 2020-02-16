import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from .constants import (
    COUNTRIES,
    CURRENCIES,
    INVOICE_TYPES,
    PAYMENT_CONDITIONS,
    PAYMENT_METHODS,
    TAX_REGIMES,
    TRANSMISSION_FORMATS,
)
from .xml import invoice_to_xml


class Address(models.Model):
    address = models.CharField(_("Address"), max_length=200)
    postcode = models.CharField(_("Post Code"), max_length=20)
    city = models.CharField(_("City"), max_length=100)
    province = models.CharField(_("Province"), max_length=100, blank=True)
    country_code = models.CharField(_("Country Code"), max_length=2, choices=COUNTRIES)

    def __str__(self):
        return (
            f"{self.address}{f' {self.city}' if self.city else ''}"
            f"{f' ({self.province})' if self.province else ''}"
            f" [{self.country_code}]"
        )


class Sender(TimeStampedModel):
    """Model containing information about a Sender of an electronic invoice.

    Contains also the configuration for the SdI."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Name"), max_length=100, unique=True)
    country_code = models.CharField(_("Country Code"), max_length=2, choices=COUNTRIES)

    contact_phone = models.CharField(_("Contact Phone"), max_length=20)
    contact_email = models.CharField(_("Contact Email"), max_length=200)

    fiscal_code = models.CharField(_("Fiscal Code"), max_length=16)
    code = models.CharField(_("Sender VAT Number"), max_length=13)

    company_name = models.CharField(_("Company Name"), max_length=80)

    tax_regime = models.CharField(_("Tax Regime"), choices=TAX_REGIMES, max_length=4)

    address = models.ForeignKey(Address, models.PROTECT, verbose_name=_("Address"))

    def __str__(self):
        return f"{self.name}"


class Item(models.Model):
    row = models.SmallIntegerField(_("Item number"))
    description = models.CharField(_("Description"), max_length=128)
    quantity = models.IntegerField(_("Quantity"))
    unit_price = models.DecimalField(_("Unit price"), max_digits=8, decimal_places=2)
    vat_rate = models.DecimalField(_("Tax"), max_digits=4, decimal_places=2)
    invoice = models.ForeignKey(
        "Invoice", related_name="items", on_delete=models.CASCADE, null=True
    )

    @property
    def total_price(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.row}. {self.description} [{self.quantity}*{self.unit_price}]"


class Invoice(TimeStampedModel):
    sender = models.ForeignKey(
        Sender, verbose_name=_("Sender"), on_delete=models.PROTECT
    )
    invoice_number = models.CharField(_("Invoice number"), max_length=20)
    invoice_type = models.CharField(
        _("Invoice type"), choices=INVOICE_TYPES, max_length=4
    )
    invoice_currency = models.CharField(
        _("Invoice currency"), choices=CURRENCIES, max_length=4
    )
    invoice_date = models.DateField(_("Invoice date"))
    invoice_deadline = models.DateField(_("Invoice deadline"))
    invoice_tax_rate = models.DecimalField(
        _("Invoice tax rate"), max_digits=5, decimal_places=2
    )
    invoice_amount = models.DecimalField(
        _("Invoice amount"), max_digits=10, decimal_places=2
    )
    invoice_tax_amount = models.DecimalField(
        _("Invoice tax"), max_digits=10, decimal_places=2
    )

    transmission_format = models.CharField(
        _("Transmission format"), choices=TRANSMISSION_FORMATS, max_length=5
    )

    payment_condition = models.CharField(
        _("Payment condition"), choices=PAYMENT_CONDITIONS, max_length=5
    )

    payment_method = models.CharField(
        _("Payment method"), choices=PAYMENT_METHODS, max_length=5
    )

    causal = models.TextField(_("Causal"), blank=True)

    recipient_tax_code = models.CharField(_("Tax code"), blank=True, max_length=16)
    recipient_denomination = models.CharField(
        _("Recipient denomination"), blank=True, max_length=80
    )
    recipient_first_name = models.CharField(
        _("Recipient first name"), blank=True, max_length=60
    )
    recipient_last_name = models.CharField(
        _("Recipient last name"), blank=True, max_length=60
    )
    recipient_code = models.CharField(_("Recipient code"), blank=True, max_length=7)
    recipient_pec = models.EmailField(_("Recipient PEC"), blank=True)
    recipient_address = models.ForeignKey(
        Address, models.PROTECT, verbose_name=_("Recipient Address")
    )

    @property
    def invoice_summary(self):
        result = list()
        for item in sorted(self.items.iterator(), key=lambda i: i.row):
            result.append(
                {
                    "row": item.row,
                    "description": item.description,
                    "quantity": item.quantity,
                    "unit_price": float(item.unit_price),
                    "total_price": float(item.total_price),
                    "vat_rate": float(item.vat_rate),
                }
            )
        return result

    def to_xml(self):
        return invoice_to_xml(self)

    def get_filename(self):
        return f"{self.invoice_number}.xml"

    def __str__(self):
        return (
            f"[{INVOICE_TYPES[self.invoice_type].title()}/{self.invoice_number}] "
            + (
                f"{f'{self.recipient_first_name} {self.recipient_last_name}'}"
                if self.recipient_first_name and self.recipient_last_name
                else f"{self.recipient_code}"
            )
            + f"{f': {self.causal}' if self.causal else ''}"
        )

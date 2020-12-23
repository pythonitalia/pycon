from datetime import date, timedelta
from decimal import Decimal

from admin_views.admin import AdminViews
from conferences.models import Conference
from django.contrib import admin, messages
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from pretix import get_invoices, get_orders

from .constants import (
    INVOICE_TYPES,
    PAYMENT_CONDITIONS,
    PAYMENT_METHODS,
    TRANSMISSION_FORMATS,
)
from .models import Address, Invoice, Item, Sender
from .utils import xml_to_string, zip_files


def invoice_export_to_xml(modeladmin, request, queryset):
    if len(queryset) == 1:
        model = queryset[0]
        file = xml_to_string(model.to_xml())
        response = HttpResponse(file, content_type="text/xml")
        response["Content-Disposition"] = f"attachment; filename={model.get_filename()}"
        response["Content-Length"] = len(file)
        return response

    files = []
    for model in queryset:
        files.append((model.get_filename(), xml_to_string(model.to_xml())))
    archive = zip_files(files)
    response = HttpResponse(archive, content_type="application/zip")
    response["Content-Disposition"] = "attachment; filename=invoices.zip"
    response["Content-Length"] = len(archive)
    return response


invoice_export_to_xml.short_description = _("Export as xml")  # type: ignore


class MissingFiscalCodeError(Exception):
    pass


class MissingTaxCodeError(Exception):
    pass


def get_tax(line):
    value = float(line["gross_value"])
    return value - value / 1.22


@transaction.atomic
def create_invoice_from_pretix(invoice, sender, order):
    invoice_date = date.fromisoformat(invoice["date"])

    confirmed_payment_providers = [payment["provider"] for payment in order["payments"]]

    if not confirmed_payment_providers:
        print(f'Skipping {invoice["number"]}')

        return

    payment_provider = confirmed_payment_providers[-1]

    invoice_type = (
        INVOICE_TYPES.TD04 if invoice["is_cancellation"] else INVOICE_TYPES.TD01
    )

    payment_method = (
        PAYMENT_METHODS.MP05
        if payment_provider == "banktransfer"
        else PAYMENT_METHODS.MP08
    )

    amount = sum([Decimal(line["gross_value"]) for line in invoice["lines"]])
    tax_amount = sum([get_tax(line) for line in invoice["lines"]])

    invoice_address = order["invoice_address"]

    first_name, *last_name_parts = invoice_address["name"].split(" ")
    last_name = " ".join(last_name_parts)

    address, _ = Address.objects.get_or_create(
        address=invoice_address["street"],
        postcode=invoice_address["zipcode"],
        city=invoice_address["city"],
        province=invoice_address["state"],
        country_code=invoice_address["country"],
    )

    recipient_fiscal_code = ""
    tax_code = ""

    if invoice_address["country"].lower() == "it":
        # if we are sending invoices to an italian recipient
        # we need to check if they have a vat number
        if invoice_address["is_business"]:
            # in that case the recipient_code should be set on the order
            # and our tax_code becomes the VAT number
            recipient_code = ""  # TODO (internal reference field?)
            tax_code = invoice_address["vat_id"]

            if not tax_code:
                raise MissingTaxCodeError(order)

        else:
            # otherwise the recipient_code is 0000000
            # and our recipient_fiscal_code becomes the italian fiscal code
            recipient_code = "0000000"
            recipient_fiscal_code = invoice_address["internal_reference"]

            if not recipient_fiscal_code:
                raise MissingFiscalCodeError(order)
    else:
        recipient_code = "XXXXXXX"
        tax_code = "99999999999"

    invoice_object, created = Invoice.objects.update_or_create(
        sender=sender,
        invoice_number=invoice["number"],
        defaults={
            "invoice_type": invoice_type,
            "is_business": invoice_address["is_business"],
            "invoice_currency": "EUR",
            "invoice_date": invoice_date,
            "invoice_deadline": invoice_date + timedelta(days=30),
            # TODO: should be invoice["lines"][0]["tax_rate"] but hotels are broken
            "invoice_tax_rate": "22.00",
            "invoice_amount": amount,
            "invoice_tax_amount": tax_amount,
            "transmission_format": TRANSMISSION_FORMATS.FPR12,
            "payment_condition": PAYMENT_CONDITIONS.TP02,
            "payment_method": payment_method,
            "recipient_denomination": invoice_address.get("company") or "",
            "recipient_first_name": first_name,
            "recipient_last_name": last_name,
            "recipient_address": address,
            "recipient_tax_code": tax_code or recipient_fiscal_code,
            "recipient_code": recipient_code,
        },
    )

    if not created:
        invoice_object.items.all().delete()

    for line in invoice["lines"]:
        Item.objects.create(
            row=line["position"],
            description=line["description"],
            quantity=1,
            # prices need to be vat_excluded
            unit_price=float(line["gross_value"]) - get_tax(line),
            # TODO: should be line["tax_rate"] but hotels are broken
            vat_rate="22.00",
            invoice=invoice_object,
        )


class InvoiceItemInline(admin.StackedInline):
    model = Item
    extra = 1


@admin.register(Invoice)
class InvoiceAdmin(AdminViews):
    actions = [invoice_export_to_xml]
    exclude = ("items",)
    inlines = [InvoiceItemInline]
    list_display = (
        "invoice_number",
        "invoice_type",
        "recipient_first_name",
        "recipient_last_name",
        "recipient_tax_code",
        "recipient_code",
    )
    admin_views = (("Sync invoices from pretix", "sync_invoices_from_pretix"),)

    def sync_invoices_from_pretix(self, request, **kwargs):
        orders = get_orders(Conference.objects.get(code="pycon11"))
        invoices = get_invoices(Conference.objects.get(code="pycon11"))

        sender = Sender.objects.first()  # TODO: conference based

        orders = {order["code"]: order for order in orders}

        for invoice in invoices:
            order = orders.get(invoice["order"])

            try:
                create_invoice_from_pretix(invoice, sender, order=order)
            except MissingFiscalCodeError:
                self.message_user(
                    request,
                    f'Missing fiscal code for {order["code"]}',
                    level=messages.WARNING,
                )
            except MissingTaxCodeError:
                self.message_user(
                    request,
                    f'Missing tax code for {order["code"]}',
                    level=messages.WARNING,
                )

        self.message_user(request, "Updated all the invoices", level=messages.SUCCESS)

        return redirect("admin:index")


admin.site.register(Sender)
admin.site.register(Address)
admin.site.register(Item)

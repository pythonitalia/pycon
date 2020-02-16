from datetime import date, timedelta
from decimal import Decimal

from admin_views.admin import AdminViews
from conferences.models import Conference
from django.contrib import admin, messages
from django.db import transaction
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from pretix import get_invoices, get_orders

from .constants import (
    INVOICE_TYPES,
    PAYMENT_CONDITIONS,
    PAYMENT_METHODS,
    TRANSMISSION_FORMATS,
)
from .models import Address, Invoice, Item, Sender
from .utils import xml_to_string, zip_files

# from django.shortcuts import redirect


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


@transaction.atomic
def create_invoice_from_pretix(invoice, sender, order):
    invoice_date = date.fromisoformat(invoice["date"])

    confirmed_payment_providers = [
        payment["provider"]
        for payment in order["payments"]
        if payment["state"] == "confirmed"
    ]

    if not confirmed_payment_providers:
        print(f'Skipping {invoice["number"]}')

        return

    payment_provider = confirmed_payment_providers[-1]

    tax_rate = invoice["lines"][0]["tax_rate"]
    payment_method = (
        PAYMENT_METHODS.MP05
        if payment_provider == "banktransfer"
        else PAYMENT_METHODS.MP08
    )

    amount = sum([Decimal(line["gross_value"]) for line in invoice["lines"]])
    tax_amount = sum([Decimal(line["tax_value"]) for line in invoice["lines"]])

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

    Invoice.objects.update_or_create(
        sender=sender,
        invoice_number=invoice["number"],
        defaults={
            "invoice_type": INVOICE_TYPES.TD01,
            "invoice_currency": "EUR",
            "invoice_date": invoice_date,
            "invoice_deadline": invoice_date + timedelta(days=30),
            "invoice_tax_rate": tax_rate,
            "invoice_amount": amount,
            "invoice_tax_amount": tax_amount,
            "transmission_format": TRANSMISSION_FORMATS.FPA12,
            "payment_condition": PAYMENT_CONDITIONS.TP02,
            "payment_method": payment_method,
            "recipient_denomination": invoice_address.get("company") or "",
            "recipient_first_name": first_name,
            "recipient_last_name": last_name,
            "recipient_tax_code": "123123",
            "recipient_code": "000000",
            "recipient_address": address,
        },
    )


class InvoiceItemInline(admin.StackedInline):
    model = Item
    extra = 1


@admin.register(Invoice)
class InvoiceAdmin(AdminViews):
    actions = [invoice_export_to_xml]
    exclude = ("items",)
    inlines = [InvoiceItemInline]
    admin_views = (("Sync invoices from pretix", "sync_invoices_from_pretix"),)

    def sync_invoices_from_pretix(self, request, **kwargs):
        # TODO: pagination
        orders = get_orders(Conference.objects.get(code="pycon11"))
        invoices = get_invoices(Conference.objects.get(code="pycon11"))

        sender = Sender.objects.first()  # TODO: conference based

        orders = {order["code"]: order for order in orders["results"]}

        for invoice in invoices["results"]:
            order = orders.get(invoice["order"])

            if not order:
                print(
                    f'Skipping invoice {invoice["number"]} for '
                    f'missing order {invoice["order"]}'
                )

                continue

            create_invoice_from_pretix(invoice, sender, order=order)

        self.message_user(request, "Updated all the invoices", level=messages.SUCCESS)

        # return redirect("admin:index")


admin.site.register(Sender)
admin.site.register(Address)
admin.site.register(Item)

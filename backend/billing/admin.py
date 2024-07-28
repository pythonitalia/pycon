from django.contrib import admin

from billing.models import BillingAddress


@admin.register(BillingAddress)
class BillingAddressAdmin(admin.ModelAdmin):
    autocomplete_fields = ["user", "organizer"]
    list_filter = ["organizer"]
    list_display = (
        "user",
        "organizer",
    )

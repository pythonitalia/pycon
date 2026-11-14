from django.contrib import admin

from custom_admin.admin import HTTPS_URL_FORMFIELD_OVERRIDES


from .models import BadgeScan


@admin.register(BadgeScan)
class BadgeScanAdmin(admin.ModelAdmin):
    formfield_overrides = HTTPS_URL_FORMFIELD_OVERRIDES
    autocomplete_fields = (
        "scanned_by",
        "scanned_user",
        "conference",
    )

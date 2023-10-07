from django.contrib import admin


from .models import BadgeScan


@admin.register(BadgeScan)
class BadgeScanAdmin(admin.ModelAdmin):
    autocomplete_fields = (
        "scanned_by",
        "scanned_user",
        "conference",
    )

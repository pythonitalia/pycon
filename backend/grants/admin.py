from django.contrib import admin
from import_export.admin import ExportMixin
from import_export.resources import ModelResource

from .models import Grant


class VoteResource(ModelResource):
    class Meta:
        model = Grant


@admin.register(Grant)
class GrantAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "email",
        "full_name",
        "conference",
        "travelling_from",
        "age",
        "gender",
        "occupation",
        "grant_type",
        "python_usage",
        "been_to_other_events",
        "interested_in_volunteering",
        "needs_funds_for_travel",
        "why",
        "notes",
    )

    list_filter = (
        "conference",
        "occupation",
        "grant_type",
        "interested_in_volunteering",
    )
    search_fields = (
        "email",
        "full_name",
        "travelling_from",
        "been_to_other_events",
        "why",
        "notes",
    )

from django.contrib import admin

from .models import Grant


@admin.register(Grant)
class GrantAdmin(admin.ModelAdmin):
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

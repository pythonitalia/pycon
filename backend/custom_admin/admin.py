from django.contrib import messages
from functools import wraps

from typing import List

from django.contrib import admin
from django.urls import path

SITE_NAME = "PyCon Italia"

admin.site.site_header = SITE_NAME
admin.site.site_title = SITE_NAME


class CustomIndexLinks(admin.ModelAdmin):
    def get_index_links(self) -> List:
        return getattr(self, "index_links", [])

    def get_urls(self) -> List:
        base_urls = super().get_urls()
        index_links = self.get_index_links()
        additional_urls = []

        for index_link in index_links:
            func_name = index_link[1]
            additional_urls.append(
                path(
                    func_name,
                    self.admin_site.admin_view(
                        getattr(self, func_name),
                    ),
                    name=f"custom_index_link_{func_name}",
                )
            )
        return base_urls + additional_urls


def validate_single_conference_selection(func):
    """
    Ensure all selected grants in the queryset belong to the same conference.
    """

    @wraps(func)
    def wrapper(modeladmin, request, queryset):
        is_filtered_by_conference = (
            queryset.values_list("conference_id").distinct().count() == 1
        )

        if not is_filtered_by_conference:
            messages.error(request, "Please select only one conference")
            return

        return func(modeladmin, request, queryset)

    return wrapper

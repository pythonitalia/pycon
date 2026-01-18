from django.db.models import F
from django.contrib import messages
from functools import wraps


from django.contrib import admin
from django.urls import path

from custom_admin.audit import create_change_admin_log_entry

SITE_NAME = "PyCon Italia"

admin.site.site_header = SITE_NAME
admin.site.site_title = SITE_NAME


class CustomIndexLinks(admin.ModelAdmin):
    def get_index_links(self) -> list:
        return getattr(self, "index_links", [])

    def get_urls(self) -> list:
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
        return additional_urls + base_urls


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


@admin.action(description="Confirm pending status change")
@validate_single_conference_selection
def confirm_pending_status(modeladmin, request, queryset):
    """
    Efficiently bulk-update status with pending_status, and accurately log the change per object.
    """
    # Use values_list to fetch ids and old statuses before updating.
    changed_objs_info = list(queryset.values_list("pk", "status", "pending_status"))

    # Perform the bulk update.
    queryset.update(
        status=F("pending_status"),
        pending_status=None,
    )

    model = queryset.model
    for pk, old_status, pending_status in changed_objs_info:
        obj = model.objects.get(pk=pk)
        create_change_admin_log_entry(
            request.user,
            obj,
            change_message=(
                f"[Bulk Admin Action] Status changed from '{old_status}' to '{pending_status}'."
            ),
        )


@admin.action(description="Reset pending status to status")
@validate_single_conference_selection
def reset_pending_status_back_to_status(modeladmin, request, queryset):
    """
    Efficiently bulk-reset pending_status to None, and accurately log the change per object.
    """
    changed_objs_info = list(queryset.values_list("pk", "pending_status"))

    queryset.update(
        pending_status=None,
    )

    model = queryset.model
    for pk, old_pending_status in changed_objs_info:
        if old_pending_status is not None:
            obj = model.objects.get(pk=pk)
            create_change_admin_log_entry(
                request.user,
                obj,
                change_message=(
                    f"[Bulk Admin Action] pending_status reset from '{old_pending_status}' to None."
                ),
            )

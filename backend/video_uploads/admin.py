from django.utils.safestring import mark_safe
from django.contrib import admin
from django.db import transaction

from video_uploads.tasks import queue_wetransfer_to_s3_transfer_request
from video_uploads.models import WetransferToS3TransferRequest


def retry_transfer(modeladmin, request, queryset):
    for obj in queryset.exclude(status=WetransferToS3TransferRequest.Status.DONE):
        obj.status = WetransferToS3TransferRequest.Status.PENDING
        obj.save(update_fields=["status"])

        transaction.on_commit(
            lambda: queue_wetransfer_to_s3_transfer_request.delay(obj.id)
        )


@admin.register(WetransferToS3TransferRequest)
class WetransferToS3TransferRequestAdmin(admin.ModelAdmin):
    list_display = [
        "conference",
        "status",
        "wetransfer_url",
    ]
    search_fields = ["conference__name", "wetransfer_url"]
    list_filter = ["conference__name"]
    ordering = ["-created"]
    date_hierarchy = "created"
    autocomplete_fields = ["conference"]
    readonly_fields = [
        "status",
        "created",
        "started_at",
        "finished_at",
        "list_imported_files",
        "failed_reason",
        "start_import",
    ]
    actions = [retry_transfer]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "conference",
                    "wetransfer_url",
                    "start_import",
                )
            },
        ),
        (
            "Metadata",
            {
                "fields": (
                    "status",
                    "list_imported_files",
                    "failed_reason",
                    "created",
                    "started_at",
                    "finished_at",
                )
            },
        ),
    )

    def save_form(self, request, form, change):
        result = super().save_form(request, form, change)
        if "_start_transfer" in form.data:
            transaction.on_commit(
                lambda: queue_wetransfer_to_s3_transfer_request.delay(form.instance.id)
            )
        return result

    def start_import(self, obj):
        if obj.status == WetransferToS3TransferRequest.Status.PENDING:
            return mark_safe(
                '<input type="submit" name="_start_transfer" value="Start import" />'
            )
        return "Already started or done."

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status == WetransferToS3TransferRequest.Status.DONE:
            return self.readonly_fields + ["conference", "wetransfer_url"]
        return super().get_readonly_fields(request, obj)

    def list_imported_files(self, obj):
        if not obj.imported_files:
            return

        html = f"""<ul style="margin: 0;">
            {"".join(f'<li>{file}</li>' for file in obj.imported_files)}
        </ul>"""
        return mark_safe(html)

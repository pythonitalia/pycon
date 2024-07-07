from django.utils.safestring import mark_safe
from django.contrib import admin
from django.db import transaction

from video_uploads.tasks import queue_wetransfer_to_s3_transfer_request
from video_uploads.models import WetransferToS3TransferRequest


def retry_transfer(modeladmin, request, queryset):
    for obj in queryset:
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
    readonly_fields = [
        "status",
        "created",
        "started_at",
        "finished_at",
        "list_imported_files",
    ]
    actions = [retry_transfer]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "conference",
                    "wetransfer_url",
                )
            },
        ),
        (
            "Metadata",
            {
                "fields": (
                    "status",
                    "failed_reason",
                    "created",
                    "started_at",
                    "finished_at",
                    "list_imported_files",
                )
            },
        ),
    )

    def list_imported_files(self, obj):
        html = f"""<ul style="margin: 0;">
            {"".join(f'<li>{file}</li>' for file in obj.imported_files)}
        </ul>"""
        return mark_safe(html)

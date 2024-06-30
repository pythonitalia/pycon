from django.contrib import messages
from django.contrib import admin

from files_upload.models import File
from files_upload.tasks import post_process_file_upload


@admin.action(description="Send files to post processing")
def send_to_post_processing(modeladmin, request, queryset):
    for file in queryset:
        post_process_file_upload.delay(file.id)

    messages.success(request, "Sent files to post processing.")


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    add_form_template = "admin/files_upload/file/add_form.html"

    list_display = ("id", "file", "created", "uploaded_by")
    search_fields = (
        "file",
        "uploaded_by",
        "id",
    )
    list_filter = ("created", "type", "virus", "mime_type")
    ordering = ("-created",)
    date_hierarchy = "created"
    autocomplete_fields = ("uploaded_by",)
    actions = [
        send_to_post_processing,
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("uploaded_by")

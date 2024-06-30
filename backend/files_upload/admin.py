from django.contrib import admin

from files_upload.models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    add_form_template = "admin/files_upload/file/add_form.html"

    list_display = ("id", "file", "created", "uploaded_by")
    search_fields = ("file", "uploaded_by")
    list_filter = ("created", "type", "virus", "mime_type")
    ordering = ("-created",)
    date_hierarchy = "created"
    autocomplete_fields = ("uploaded_by",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("uploaded_by")

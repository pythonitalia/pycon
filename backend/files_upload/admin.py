from django.contrib import admin

from files_upload.models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "created", "uploaded_by")
    search_fields = ("file", "uploaded_by")
    list_filter = ("created",)
    ordering = ("-created",)
    date_hierarchy = "created"
    autocomplete_fields = ("uploaded_by",)

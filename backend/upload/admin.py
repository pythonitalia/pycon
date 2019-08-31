from django.contrib import admin
from upload.models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ("file", "date_upload")
    search_filters = ("file", "date_upload")

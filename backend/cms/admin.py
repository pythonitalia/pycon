from django.contrib import admin

from .models import GenericCopy


@admin.register(GenericCopy)
class GenericCopyAdmin(admin.ModelAdmin):
    list_display = ("key", "content", "conference")

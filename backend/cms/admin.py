from django.contrib import admin

from .models import FAQ, GenericCopy


@admin.register(GenericCopy)
class GenericCopyAdmin(admin.ModelAdmin):
    list_display = ("key", "content", "conference")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("conference",)

from django.contrib import admin

from organizers.models import Organizer


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("created",)
    readonly_fields = ("created", "modified")
    prepopulated_fields = {"slug": ("name",)}

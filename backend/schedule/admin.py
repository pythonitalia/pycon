from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Room, ScheduleItem


@admin.register(ScheduleItem)
class ScheduleItemAdmin(admin.ModelAdmin):
    list_display = ("title", "conference", "start", "end", "type", "submission")
    ordering = ("conference", "start")
    fieldsets = (
        (
            _("Event"),
            {
                "fields": (
                    "conference",
                    "type",
                    "title",
                    "image",
                    "highlight_color",
                    "description",
                    "submission",
                    "additional_speakers",
                )
            },
        ),
        (_("Schedule"), {"fields": ("start", "end", "rooms")}),
    )
    autocomplete_fields = ("submission",)
    filter_horizontal = ("rooms", "additional_speakers")


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "conference")
    list_filter = ("conference",)

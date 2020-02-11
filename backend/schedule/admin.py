from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from ordered_model.admin import OrderedModelAdmin

from .models import Day, Room, ScheduleItem, Slot


class SlotInline(admin.TabularInline):
    model = Slot


@admin.register(ScheduleItem)
class ScheduleItemAdmin(admin.ModelAdmin):
    list_display = ("title", "conference", "slot", "type", "submission")
    ordering = ("conference", "slot")
    fieldsets = (
        (
            _("Event"),
            {
                "fields": (
                    "conference",
                    "type",
                    "title",
                    "slug",
                    "image",
                    "highlight_color",
                    "description",
                    "submission",
                    "additional_speakers",
                )
            },
        ),
        (_("Schedule"), {"fields": ("slot", "duration", "rooms")}),
    )
    autocomplete_fields = ("submission",)
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("rooms", "additional_speakers")


@admin.register(Room)
class RoomAdmin(OrderedModelAdmin):
    list_display = ("name", "conference")
    list_filter = ("conference",)


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ("day", "conference")
    list_filter = ("conference",)
    inlines = (SlotInline,)

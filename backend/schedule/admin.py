from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from ordered_model.admin import (
    OrderedInlineModelAdminMixin,
    OrderedModelAdmin,
    OrderedTabularInline,
)

from users.autocomplete import UsersBackendAutocomplete

from .models import (
    Day,
    DayRoomThroughModel,
    Room,
    ScheduleItem,
    ScheduleItemAdditionalSpeaker,
    Slot,
)


class SlotInline(admin.TabularInline):
    model = Slot


class ScheduleItemAdditionalSpeakerInlineForm(forms.ModelForm):
    class Meta:
        model = ScheduleItemAdditionalSpeaker
        widgets = {
            "user_id": UsersBackendAutocomplete(admin.site),
        }
        fields = ["scheduleitem", "user_id"]


class ScheduleItemAdditionalSpeakerInline(admin.TabularInline):
    model = ScheduleItemAdditionalSpeaker
    form = ScheduleItemAdditionalSpeakerInlineForm


@admin.register(ScheduleItem)
class ScheduleItemAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "conference",
        "status",
        "language",
        "slot",
        "type",
        "submission",
    )
    list_filter = ("conference", "status", "type")
    ordering = ("conference", "slot")
    fieldsets = (
        (
            _("Event"),
            {
                "fields": (
                    "conference",
                    "type",
                    "status",
                    "language",
                    "title",
                    "slug",
                    "image",
                    "highlight_color",
                    "audience_level",
                    "description",
                    "submission",
                )
            },
        ),
        (_("Schedule"), {"fields": ("slot", "duration", "rooms")}),
    )
    autocomplete_fields = ("submission",)
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("rooms",)
    inlines = [
        ScheduleItemAdditionalSpeakerInline,
    ]


@admin.register(Room)
class RoomAdmin(OrderedModelAdmin):
    list_display = ("name", "conference")
    list_filter = ("conference",)


class DayRoomThroughModelInline(OrderedTabularInline):
    model = DayRoomThroughModel
    fields = (
        "room",
        "order",
        "move_up_down_links",
    )
    readonly_fields = (
        "order",
        "move_up_down_links",
    )


@admin.register(Day)
class DayAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):
    list_display = ("day", "conference")
    list_filter = ("conference",)
    inlines = (SlotInline, DayRoomThroughModelInline)

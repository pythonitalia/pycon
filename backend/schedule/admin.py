from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from ordered_model.admin import (
    OrderedInlineModelAdminMixin,
    OrderedModelAdmin,
    OrderedTabularInline,
)

from domain_events.publisher import send_schedule_invitation_email
from users.autocomplete import UsersBackendAutocomplete

from .models import (
    Day,
    DayRoomThroughModel,
    Room,
    ScheduleItem,
    ScheduleItemAdditionalSpeaker,
    Slot,
)


@admin.action(description="Send schedule invitation")
def send_schedule_invitation(modeladmin, request, queryset):
    # We only want to send it to those we are still waiting for confirmation
    # and that have a submission
    queryset = queryset.filter(
        status=ScheduleItem.STATUS.waiting_confirmation,
        submission__isnull=False,
        type=ScheduleItem.TYPES.submission,
    )

    for schedule_item in queryset:
        send_schedule_invitation_email(schedule_item)


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
        (_("Invitation"), {"fields": ("speaker_invitation_notes",)}),
    )
    autocomplete_fields = ("submission",)
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("rooms",)
    inlines = [
        ScheduleItemAdditionalSpeakerInline,
    ]
    actions = [
        send_schedule_invitation,
    ]


class ScheduleItemInvitationProxy(ScheduleItem):
    class Meta:
        proxy = True
        verbose_name = _("Schedule invitation")
        verbose_name_plural = _("Schedule invitations")


@admin.register(ScheduleItemInvitationProxy)
class ScheduleItemInvitationProxyAdmin(admin.ModelAdmin):
    list_display = (
        "slot",
        "status",
        "title",
        "conference",
        "speaker_invitation_notes",
        "open_schedule_item",
        "open_submission",
    )
    list_filter = (
        "conference",
        "slot",
        "status",
    )
    list_display_links = None

    def open_schedule_item(self, obj) -> str:
        url = reverse("admin:schedule_scheduleitem_change", args=[obj.id])
        return mark_safe(f'<a class="button" target="_blank" href="{url}">Schedule</a>')

    def open_submission(self, obj) -> str:
        url = reverse("admin:submissions_submission_change", args=[obj.id])
        return mark_safe(
            f'<a class="button" target="_blank" href="{url}">Submission</a>'
        )

    def has_add_permission(self, *args, **kwargs) -> bool:
        return False

    def has_delete_permission(self, *args, **kwargs) -> bool:
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(
            submission__isnull=False,
        ).order_by("slot__day", "slot__hour")


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

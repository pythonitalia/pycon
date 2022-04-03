from django import forms
from django.contrib import admin, messages
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from ordered_model.admin import (
    OrderedInlineModelAdminMixin,
    OrderedModelAdmin,
    OrderedTabularInline,
)

from conferences.models import SpeakerVoucher
from domain_events.publisher import (
    send_new_submission_time_slot,
    send_schedule_invitation_email,
)
from users.autocomplete import UsersBackendAutocomplete

from .models import (
    Day,
    DayRoomThroughModel,
    Room,
    ScheduleItem,
    ScheduleItemAdditionalSpeaker,
    ScheduleItemAttendee,
    ScheduleItemInvitation,
    Slot,
)


@admin.action(description="Mark Speakers to receive Vouchers")
def mark_speakers_to_receive_vouchers(modeladmin, request, queryset):
    queryset = queryset.filter(
        submission__isnull=False,
        type__in=[
            ScheduleItem.TYPES.submission,
            ScheduleItem.TYPES.training,
        ],
    )

    is_filtered_by_conference = (
        queryset.values_list("conference_id").distinct().count() == 1
    )

    if not is_filtered_by_conference:
        messages.error(request, "Please select only one conference")
        return

    conference = queryset.only("conference_id").first().conference

    excluded_speakers = (
        queryset.filter(exclude_from_voucher_generation=True)
        .values_list("submission__speaker_id", flat=True)
        .distinct()
    )

    existing_vouchers_users = SpeakerVoucher.objects.filter(
        conference_id=conference.id,
    ).values_list("user_id", flat=True)

    created_codes = 0

    for schedule_item in (
        queryset.exclude(submission__speaker_id__in=existing_vouchers_users)
        .exclude(submission__speaker_id__in=excluded_speakers)
        .order_by("submission__speaker_id")
    ):
        if SpeakerVoucher.objects.filter(
            conference_id=schedule_item.conference_id,
            user_id=schedule_item.submission.speaker_id,
        ).exists():
            continue

        SpeakerVoucher.objects.create(
            conference_id=schedule_item.conference_id,
            user_id=schedule_item.submission.speaker_id,
            voucher_code=SpeakerVoucher.generate_code(),
        )

        created_codes = created_codes + 1

    messages.info(request, f"Created {created_codes} new vouchers")


@admin.action(description="Send schedule invitation to all (waiting confirmation)")
def send_schedule_invitation_to_all(modeladmin, request, queryset):
    _send_invitations(queryset=queryset)
    messages.add_message(request, messages.INFO, "Invitations sent")


@admin.action(description="Send reminder to waiting confirmation invitations")
def send_schedule_invitation_reminder_to_waiting(modeladmin, request, queryset):
    _send_invitations(queryset=queryset, invited_only=True, is_reminder=True)
    messages.add_message(request, messages.INFO, "Invitations reminder sent")


@admin.action(
    description="Send schedule invitation to uninvited (waiting confirmation)"
)
def send_schedule_invitation_to_uninvited(modeladmin, request, queryset):
    _send_invitations(queryset=queryset, uninvited_only=True)
    messages.add_message(request, messages.INFO, "Invitations sent")


def _send_invitations(
    *,
    queryset,
    invited_only: bool = False,
    uninvited_only: bool = False,
    is_reminder: bool = False,
):
    # We only want to send it to those we are still waiting for confirmation
    # and that have a submission

    queryset = queryset.filter(
        status=ScheduleItem.STATUS.waiting_confirmation,
        submission__isnull=False,
        type__in=[
            ScheduleItem.TYPES.submission,
            ScheduleItem.TYPES.training,
        ],
    )

    if uninvited_only:
        queryset = queryset.filter(speaker_invitation_sent_at__isnull=True)
    elif invited_only:
        queryset = queryset.filter(speaker_invitation_sent_at__isnull=False)

    for schedule_item in queryset:
        schedule_item.speaker_invitation_sent_at = timezone.now()
        send_schedule_invitation_email(schedule_item, is_reminder=is_reminder)
        schedule_item.save()


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


class ScheduleItemAttendeeInlineForm(forms.ModelForm):
    class Meta:
        model = ScheduleItemAttendee
        widgets = {
            "user_id": UsersBackendAutocomplete(admin.site),
        }
        fields = ["schedule_item", "user_id"]


class ScheduleItemAttendeeInline(admin.TabularInline):
    model = ScheduleItemAttendee
    form = ScheduleItemAttendeeInlineForm


class ScheduleItemAdminForm(forms.ModelForm):
    new_slot = forms.ModelChoiceField(
        queryset=Slot.objects.all(), required=False, empty_label="(Don't move)"
    )
    notify_new_time_slot = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["slot"].queryset = (
            self.fields["slot"]
            .queryset.filter(day__conference_id=self.instance.conference_id)
            .order_by("day__day", "hour")
        )

        self.fields["new_slot"].queryset = (
            self.fields["new_slot"]
            .queryset.filter(day__conference_id=self.instance.conference_id)
            .order_by("day__day", "hour")
        )

        self.fields["submission"].queryset = self.fields["submission"].queryset.filter(
            conference_id=self.instance.conference_id
        )

        self.fields["keynote"].queryset = self.fields["keynote"].queryset.filter(
            conference_id=self.instance.conference_id
        )

    class Meta:
        model = ScheduleItem
        fields = (
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
            "slot",
            "new_slot",
            "notify_new_time_slot",
            "duration",
            "rooms",
            "keynote",
            "speaker_invitation_notes",
            "speaker_invitation_sent_at",
            "attendees_total_capacity",
        )


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
    form = ScheduleItemAdminForm
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
                    "keynote",
                )
            },
        ),
        (
            _("Schedule"),
            {
                "fields": (
                    "slot",
                    "new_slot",
                    "notify_new_time_slot",
                    "duration",
                    "rooms",
                )
            },
        ),
        (
            _("Invitation"),
            {"fields": ("speaker_invitation_notes", "speaker_invitation_sent_at")},
        ),
        (_("Booking"), {"fields": ("attendees_total_capacity", "spaces_left")}),
        (_("Voucher"), {"fields": ("exclude_from_voucher_generation",)}),
    )
    autocomplete_fields = ("submission",)
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("rooms",)
    inlines = [
        ScheduleItemAdditionalSpeakerInline,
        ScheduleItemAttendeeInline,
    ]
    actions = [
        send_schedule_invitation_to_all,
        send_schedule_invitation_to_uninvited,
        send_schedule_invitation_reminder_to_waiting,
        mark_speakers_to_receive_vouchers,
    ]
    readonly_fields = ("spaces_left",)

    def spaces_left(self, obj):
        if obj.attendees_total_capacity is None:
            return None

        return obj.attendees_total_capacity - obj.attendees.count()

    def save_form(self, request, form, change):
        if form.cleaned_data["new_slot"]:
            form.instance.slot = form.cleaned_data["new_slot"]

        return_value = super().save_form(request, form, change)

        if form.cleaned_data["notify_new_time_slot"]:
            send_new_submission_time_slot(form.instance)

        return return_value


@admin.register(ScheduleItemInvitation)
class ScheduleItemInvitationAdmin(admin.ModelAdmin):
    list_display = (
        "slot",
        "status",
        "title",
        "conference",
        "speaker_invitation_notes",
        "speaker_invitation_sent_at",
        "open_schedule_item",
        "open_submission",
    )
    list_filter = (
        "conference",
        "status",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slot",
                    "status",
                    "speaker_invitation_notes",
                    "speaker_invitation_sent_at",
                    "conference",
                    "open_schedule_item",
                    "open_submission",
                ),
            },
        ),
    )

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

    def has_change_permission(self, *args, **kwargs) -> bool:
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(
            submission__isnull=False,
        ).order_by("slot__day", "slot__hour")


@admin.register(Room)
class RoomAdmin(OrderedModelAdmin):
    list_display = (
        "name",
        "type",
    )
    list_filter = ("type",)


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

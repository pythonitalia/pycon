from import_export.resources import ModelResource
from django.db.models import Prefetch
from typing import Dict
from django import forms
from django.contrib import admin, messages
from django.db.models import Q
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from import_export.admin import ExportMixin
from import_export.fields import Field
from import_export.formats.base_formats import CSV
from ordered_model.admin import (
    OrderedInlineModelAdminMixin,
    OrderedModelAdmin,
    OrderedTabularInline,
)
from conferences.models import SpeakerVoucher
from pretix import user_has_admission_ticket
from schedule.tasks import (
    send_schedule_invitation_email,
    send_speaker_communication_email,
    send_submission_time_slot_changed_email,
)
from video_upload.workflows.batch_multiple_schedule_items_video_upload import (
    BatchMultipleScheduleItemsVideoUpload,
)
from temporal.sdk import start_workflow
from schedule.forms import EmailSpeakersForm

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
        type__in=[
            ScheduleItem.TYPES.talk,
            ScheduleItem.TYPES.training,
        ],
    )

    is_filtered_by_conference = (
        queryset.values_list("conference_id").distinct().count() == 1
    )

    if not is_filtered_by_conference:
        messages.error(request, "Please select only one conference")
        return

    excluded_speakers = (
        queryset.filter(exclude_from_voucher_generation=True)
        .values_list("submission__speaker_id", flat=True)
        .distinct()
    )

    conference = queryset.only("conference_id").first().conference

    existing_vouchers: dict[int, SpeakerVoucher.VoucherType] = {
        user_id: voucher_type
        for user_id, voucher_type in SpeakerVoucher.objects.filter(
            conference_id=conference.id,
        ).values_list("user_id", "voucher_type")
    }
    vouchers_to_create: dict[int, SpeakerVoucher.VoucherType] = {}

    created_codes = 0

    for schedule_item in (
        queryset.exclude(submission__speaker_id__in=excluded_speakers)
        .prefetch_related(
            Prefetch(
                "additional_speakers",
                queryset=ScheduleItemAdditionalSpeaker.objects.order_by("id"),
                to_attr="additional_speakers_sorted",
            )
        )
        .order_by("submission__speaker_id")
    ):
        has_main_speaker = bool(schedule_item.submission_id)

        if has_main_speaker:
            speaker_id = schedule_item.submission.speaker_id

            if not voucher_exists(existing_vouchers, speaker_id):
                # Create the voucher, if the speaker is already in the list,
                # we upgrade the voucher type to speaker
                vouchers_to_create[speaker_id] = SpeakerVoucher.VoucherType.SPEAKER
                created_codes = created_codes + 1

        first_co_speaker = (
            schedule_item.additional_speakers_sorted[0]
            if schedule_item.additional_speakers_sorted
            else None
        )
        if first_co_speaker and not voucher_exists(
            existing_vouchers, first_co_speaker.user_id
        ):
            voucher_type = (
                SpeakerVoucher.VoucherType.CO_SPEAKER
                if has_main_speaker
                else SpeakerVoucher.VoucherType.SPEAKER
            )
            vouchers_to_create[first_co_speaker.user_id] = voucher_type

            created_codes = created_codes + 1

    vouchers_objects = []
    for user_id, voucher_type in vouchers_to_create.items():
        vouchers_objects.append(
            SpeakerVoucher(
                conference_id=conference.id,
                user_id=user_id,
                voucher_code=SpeakerVoucher.generate_code(),
                voucher_type=voucher_type,
            )
        )

    SpeakerVoucher.objects.bulk_create(vouchers_objects)

    messages.info(request, f"Created {created_codes} new vouchers")


def voucher_exists(
    existing_vouchers: Dict[int, SpeakerVoucher.VoucherType],
    speaker_id: int,
) -> bool:
    return speaker_id in existing_vouchers


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
            ScheduleItem.TYPES.talk,
            ScheduleItem.TYPES.submission,
            ScheduleItem.TYPES.training,
        ],
    )

    if uninvited_only:
        queryset = queryset.filter(speaker_invitation_sent_at__isnull=True)
    elif invited_only:
        queryset = queryset.filter(speaker_invitation_sent_at__isnull=False)

    for schedule_item in queryset:
        send_schedule_invitation_email.delay(
            schedule_item_id=schedule_item.id, is_reminder=is_reminder
        )


@admin.action(description="Upload videos to YouTube")
def upload_videos_to_youtube(modeladmin, request, queryset):
    videos = queryset.filter(youtube_video_id__exact="").exclude(
        video_uploaded_path__exact=""
    )
    conference_id = queryset.first().conference_id
    start_workflow(
        workflow=BatchMultipleScheduleItemsVideoUpload.run,
        id=f"batch-upload-video-conference-{conference_id}",
        task_queue="default",
        arg=BatchMultipleScheduleItemsVideoUpload.input(
            schedule_items_ids=list(videos.values_list("id", flat=True))
        ),
    )

    messages.add_message(
        request, messages.INFO, f"Scheduled {videos.count()} videos to upload"
    )


class SlotInline(admin.TabularInline):
    model = Slot


class ScheduleItemAdditionalSpeakerInlineForm(forms.ModelForm):
    class Meta:
        model = ScheduleItemAdditionalSpeaker
        fields = ["scheduleitem", "user"]


class ScheduleItemAdditionalSpeakerInline(admin.TabularInline):
    model = ScheduleItemAdditionalSpeaker
    form = ScheduleItemAdditionalSpeakerInlineForm
    autocomplete_fields = ("user",)


class ScheduleItemAttendeeInlineForm(forms.ModelForm):
    class Meta:
        model = ScheduleItemAttendee
        fields = ["schedule_item", "user"]


class ScheduleItemAttendeeInline(admin.TabularInline):
    model = ScheduleItemAttendee
    form = ScheduleItemAttendeeInlineForm
    autocomplete_fields = ("user",)


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
            .prefetch_related("day")
        )

        self.fields["new_slot"].queryset = (
            self.fields["new_slot"]
            .queryset.filter(day__conference_id=self.instance.conference_id)
            .order_by("day__day", "hour")
            .prefetch_related("day")
        )

        self.fields["submission"].queryset = self.fields["submission"].queryset.filter(
            conference_id=self.instance.conference_id
        )

        self.fields["keynote"].queryset = self.fields["keynote"].queryset.filter(
            conference_id=self.instance.conference_id
        )

        self.fields["rooms"].queryset = self.fields["rooms"].queryset.filter(
            id__in=DayRoomThroughModel.objects.filter(
                day__conference_id=self.instance.conference_id
            ).values_list("room_id", flat=True)
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
            "slido_url",
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
                    "slido_url",
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
        (_("YouTube"), {"fields": ("youtube_video_id", "video_uploaded_path")}),
    )
    autocomplete_fields = ("submission",)
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("rooms",)
    search_fields = (
        "title",
        "submission__title",
        "submission__speaker__full_name",
        "submission__speaker__email",
    )
    inlines = [
        ScheduleItemAdditionalSpeakerInline,
        ScheduleItemAttendeeInline,
    ]
    actions = [
        send_schedule_invitation_to_all,
        send_schedule_invitation_to_uninvited,
        send_schedule_invitation_reminder_to_waiting,
        mark_speakers_to_receive_vouchers,
        upload_videos_to_youtube,
    ]
    readonly_fields = ("spaces_left",)

    def get_urls(self):
        return [
            path(
                "email-speakers/",
                self.admin_site.admin_view(self.email_speakers),
                name="schedule-email-speakers",
            ),
            path(
                "<int:object_id>/export-attendees/",
                self.admin_site.admin_view(self.export_attendees),
                name="schedule-export-attendees",
            ),
        ] + super().get_urls()

    def export_attendees(self, request, object_id: int):
        schedule_item = ScheduleItem.objects.get(id=object_id)
        resource = ScheduleItemAttendeeResource()
        data = resource.export(schedule_item.attendees.all())
        csv_format = CSV()
        export_data = csv_format.export_data(data)
        date_str = timezone.now().strftime("%Y-%m-%d")
        response = HttpResponse(export_data, content_type=csv_format.get_content_type())
        response[
            "Content-Disposition"
        ] = f'attachment; filename="{schedule_item.slug}-attendees-{date_str}.csv"'
        return response

    def email_speakers(self, request):
        form = EmailSpeakersForm(request.POST or None)
        context = dict(
            self.admin_site.each_context(request),
            form=form,
        )

        if request.method == "POST" and form.is_valid():
            conference = form.cleaned_data["conference"]
            subject = form.cleaned_data["subject"]
            body = form.cleaned_data["body"]
            only_speakers_without_ticket = form.cleaned_data[
                "only_speakers_without_ticket"
            ]

            schedule_items = conference.schedule_items.filter(
                Q(submission__isnull=False) | Q(additional_speakers__isnull=False)
            )
            notified_ids = set()

            for schedule_item in schedule_items.all():
                if (
                    schedule_item.submission_id
                    and schedule_item.submission.speaker_id not in notified_ids
                ):
                    send_speaker_communication_email.delay(
                        user_id=schedule_item.submission.speaker_id,
                        subject=subject,
                        body=body,
                        only_speakers_without_ticket=only_speakers_without_ticket,
                        conference_id=conference.id,
                    )
                    notified_ids.add(schedule_item.submission.speaker_id)

                for additional_speaker in schedule_item.additional_speakers.all():
                    if additional_speaker.user_id in notified_ids:
                        continue

                    notified_ids.add(additional_speaker.user_id)

                    send_speaker_communication_email.delay(
                        user_id=additional_speaker.user_id,
                        subject=subject,
                        body=body,
                        only_speakers_without_ticket=only_speakers_without_ticket,
                        conference_id=conference.id,
                    )

            self.message_user(
                request,
                f"Scheduled {len(notified_ids)} emails.",
                messages.SUCCESS,
            )

        return TemplateResponse(request, "email-speakers.html", context)

    def spaces_left(self, obj):
        if obj.attendees_total_capacity is None:
            return None

        return obj.attendees_total_capacity - obj.attendees.count()

    def save_form(self, request, form, change):
        if form.cleaned_data["new_slot"]:
            form.instance.slot = form.cleaned_data["new_slot"]

        return_value = super().save_form(request, form, change)

        if form.cleaned_data["notify_new_time_slot"]:
            send_submission_time_slot_changed_email.delay(
                schedule_item_id=form.instance.id
            )

        return return_value


SCHEDULE_ITEM_INVITATION_FIELDS = [
    "id",
    "title",
    "speaker_display_name",
    "speaker_email",
    "speaker_has_ticket",
    "slot__day__day",
    "slot__hour",
]


class ScheduleItemInvitationResource(ModelResource):
    search_field = "submission__speaker_id"

    speaker_display_name = Field()
    speaker_email = Field()
    speaker_has_ticket = Field()

    def dehydrate_speaker_display_name(self, obj):
        return obj.submission.speaker.display_name

    def dehydrate_speaker_email(self, obj):
        if not obj.submission.speaker_id:
            return "<no user>"

        return obj.submission.speaker.email

    def dehydrate_speaker_has_ticket(self, obj):
        if not obj.submission.speaker_id:
            return "<no user>"

        return user_has_admission_ticket(
            email=obj.submission.speaker.email,
            event_organizer=obj.conference.pretix_organizer_id,
            event_slug=obj.conference.pretix_event_id,
        )

    class Meta:
        model = ScheduleItem
        fields = SCHEDULE_ITEM_INVITATION_FIELDS
        export_order = SCHEDULE_ITEM_INVITATION_FIELDS


SCHEDULE_ITEM_ATTENDEE_FIELDS = [
    "full_name",
    "name",
    "email",
]


class ScheduleItemAttendeeResource(ModelResource):
    search_field = "user_id"

    full_name = Field()
    name = Field()
    email = Field()

    def dehydrate_email(self, obj):
        if not obj.user_id:
            return "<no user>"

        return obj.user.email

    def dehydrate_full_name(self, obj):
        if not obj.user_id:
            return "<no user>"

        return obj.user.full_name

    def dehydrate_name(self, obj):
        if not obj.user_id:
            return "<no user>"

        return obj.user.name

    class Meta:
        model = ScheduleItemAttendee
        fields = SCHEDULE_ITEM_ATTENDEE_FIELDS
        export_order = SCHEDULE_ITEM_ATTENDEE_FIELDS


@admin.register(ScheduleItemInvitation)
class ScheduleItemInvitationAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ScheduleItemInvitationResource
    list_display = (
        "slot",
        "status",
        "title",
        "speaker_display_name",
        "conference",
        "speaker_has_ticket",
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

    def speaker_display_name(self, obj):
        return obj.submission.speaker.display_name

    @admin.display(
        boolean=True,
    )
    def speaker_has_ticket(self, obj) -> bool:
        if not obj.submission.speaker_id:
            return None

        return user_has_admission_ticket(
            email=obj.submission.speaker.email,
            event_organizer=obj.conference.pretix_organizer_id,
            event_slug=obj.conference.pretix_event_id,
        )

    def open_schedule_item(self, obj) -> str:
        url = reverse("admin:schedule_scheduleitem_change", args=[obj.id])
        return mark_safe(f'<a class="button" target="_blank" href="{url}">Schedule</a>')

    def open_submission(self, obj) -> str:
        url = reverse("admin:submissions_submission_change", args=[obj.submission_id])
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
    fields = ("room", "order", "move_up_down_links", "streaming_url", "slido_url")
    readonly_fields = (
        "order",
        "move_up_down_links",
    )


@admin.register(Day)
class DayAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):
    list_display = ("day", "conference")
    list_filter = ("conference",)
    inlines = (SlotInline, DayRoomThroughModelInline)

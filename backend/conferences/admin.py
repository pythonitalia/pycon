from collections import Counter
from pathlib import Path
from django.core.files.storage import storages
from django import forms
from django.contrib import admin, messages
from django.core import exceptions
from django.core.cache import cache
from django.forms import BaseInlineFormSet
from django.forms.models import ModelForm
from django.shortcuts import redirect, render
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _
from ordered_model.admin import (
    OrderedInlineModelAdminMixin,
    OrderedModelAdmin,
    OrderedStackedInline,
    OrderedTabularInline,
)
from itertools import permutations

from conferences.models import SpeakerVoucher
from domain_events.publisher import send_speaker_voucher_email
from pretix import create_voucher
from schedule.models import ScheduleItem
from users.client import get_users_data_by_ids
from sponsors.models import SponsorLevel
from users.autocomplete import UsersBackendAutocomplete
from users.mixins import AdminUsersMixin, SearchUsersMixin
from voting.models import IncludedEvent

from .models import (
    AudienceLevel,
    Conference,
    Deadline,
    Duration,
    Keynote,
    KeynoteSpeaker,
    Topic,
)


def validate_deadlines_form(forms):
    existing_types = set()
    for form in forms:
        if not form.cleaned_data:
            return

        start = form.cleaned_data["start"]
        end = form.cleaned_data["end"]
        delete = form.cleaned_data["DELETE"]

        if start > end:
            raise exceptions.ValidationError(_("Start date cannot be after end"))

        type = form.cleaned_data["type"]

        if type == Deadline.TYPES.custom or delete:
            continue

        if type in existing_types:
            raise exceptions.ValidationError(
                _("You can only have one deadline of type %(type)s") % {"type": type}
            )

        existing_types.add(type)


class DeadlineForm(ModelForm):
    class Meta:
        model = Deadline
        fields = ["start", "end", "name", "description", "type", "conference"]


class DeadlineFormSet(BaseInlineFormSet):
    def clean(self):
        validate_deadlines_form(self.forms)


class DeadlineInline(admin.TabularInline):
    model = Deadline
    form = DeadlineForm
    formset = DeadlineFormSet


class DurationInline(admin.StackedInline):
    model = Duration
    filter_horizontal = ("allowed_submission_types",)


class SponsorLevelInline(OrderedTabularInline):
    model = SponsorLevel
    fields = ("name", "conference", "sponsors", "order", "move_up_down_links")
    readonly_fields = (
        "order",
        "move_up_down_links",
    )
    ordering = ("order",)
    extra = 1


class IncludedEventInline(admin.TabularInline):
    model = IncludedEvent


@admin.register(Conference)
class ConferenceAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):
    readonly_fields = ("created", "modified")
    filter_horizontal = ("topics", "languages", "audience_levels", "submission_types")
    fieldsets = (
        (
            "Details",
            {
                "fields": (
                    "name",
                    "code",
                    "introduction",
                    "timezone",
                    "latitude",
                    "longitude",
                    "map_link",
                )
            },
        ),
        (
            "Pretix",
            {"fields": ("pretix_organizer_id", "pretix_event_id", "pretix_event_url")},
        ),
        (
            "Speaker Voucher",
            {"fields": ("pretix_speaker_voucher_quota_id",)},
        ),
        (
            "Integrations",
            {
                "fields": (
                    "slack_new_proposal_incoming_webhook_url",
                    "slack_new_proposal_comment_incoming_webhook_url",
                    "slack_new_grant_reply_incoming_incoming_webhook_url",
                    "slack_speaker_invitation_answer_incoming_webhook_url",
                )
            },
        ),
        (
            "Hotel",
            {
                "fields": (
                    "pretix_hotel_ticket_id",
                    "pretix_hotel_room_type_question_id",
                    "pretix_hotel_checkin_question_id",
                    "pretix_hotel_checkout_question_id",
                    "pretix_hotel_bed_layout_question_id",
                )
            },
        ),
        (
            "Conference",
            {
                "fields": (
                    ("start", "end"),
                    "submission_types",
                    "topics",
                    "audience_levels",
                    "languages",
                )
            },
        ),
        (
            "Grants",
            {
                "fields": (
                    "grants_default_ticket_amount",
                    "grants_default_accommodation_amount",
                    "grants_default_travel_from_italy_amount",
                    "grants_default_travel_from_europe_amount",
                    "grants_default_travel_from_extra_eu_amount",
                )
            },
        ),
    )
    inlines = [DeadlineInline, DurationInline, SponsorLevelInline, IncludedEventInline]

    def get_urls(self):
        return super().get_urls() + [
            path(
                "<int:object_id>/video-upload/map-videos",
                self.admin_site.admin_view(self.map_videos),
                name="map_videos",
            )
        ]

    def map_videos(self, request, object_id):
        if request.method == "POST":
            data = request.POST
            if "run_matcher" in data:
                self.run_video_uploaded_path_matcher(
                    request,
                    object_id,
                    ignore_cache=data.get("ignore_cache", False) == "1",
                )
            elif "manual_changes" in data:
                self.save_manual_changes(object_id, data)

            return redirect(
                reverse("admin:map_videos", kwargs={"object_id": object_id})
            )

        all_events = (
            ScheduleItem.objects.filter(conference_id=object_id)
            .prefetch_related(
                "slot__day",
                "submission",
                "additional_speakers",
            )
            .order_by("slot__day__day", "slot__hour", "id")
            .all()
        )
        users_data = self._get_speakers_data_for_events(all_events)

        context = dict(
            self.admin_site.each_context(request),
            events=all_events,
            users_data=users_data,
        )

        return render(request, "admin/videos_upload/map_videos.html", context)

    def save_manual_changes(self, object_id, data):
        conference = Conference.objects.get(pk=object_id)
        all_events = conference.schedule_items.all()

        for event in all_events:
            video_uploaded_path = data.get(f"video_uploaded_path_{event.id}", "")
            event.video_uploaded_path = video_uploaded_path
            event.save(update_fields=["video_uploaded_path"])

    def run_video_uploaded_path_matcher(self, request, object_id, ignore_cache):
        conference = Conference.objects.get(pk=object_id)
        all_events = conference.schedule_items.prefetch_related(
            "submission", "additional_speakers"
        ).all()
        storage = storages["conferencevideos"]

        cache_key = f"{conference.code}:video-upload-files-cache"
        files = cache.get(cache_key)

        if not files or ignore_cache:
            files = list(walk_conference_videos_folder(storage, f"{conference.code}/"))
            cache.set(cache_key, files, 60 * 60 * 24 * 7)

        users_data = self._get_speakers_data_for_events(all_events)
        counter = Counter()
        used_files = set()

        for event in all_events:
            video_uploaded_path = self.match_event_to_video_file(
                event, files, users_data
            )
            event.video_uploaded_path = video_uploaded_path
            event.save(update_fields=["video_uploaded_path"])

            if video_uploaded_path:
                counter["matched"] += 1
                used_files.add(video_uploaded_path)

        self.message_user(
            request,
            f"Matched {counter['matched']} videos to events.",
            messages.SUCCESS,
        )

        unused_files = set(files).difference(used_files)
        if unused_files:
            self.message_user(
                request,
                f"Some files were not used: {', '.join(unused_files)}",
                messages.WARNING,
            )

    def match_event_to_video_file(self, event, files, users_data):
        possible_file_names = None

        if not event.submission_id:
            possible_file_names = [event.title.lower()]
        else:

            def best_name(speaker_data):
                return (speaker_data["fullname"] or speaker_data["name"]).lower()

            speaker_data = users_data[str(event.submission.speaker_id)]
            speaker_name = best_name(speaker_data)
            co_speakers_ids = [
                co_speaker.user_id for co_speaker in event.additional_speakers.all()
            ]
            co_speakers_data = [
                users_data[str(co_speaker_id)] for co_speaker_id in co_speakers_ids
            ]
            co_speakers_names = [
                best_name(co_speaker_data) for co_speaker_data in co_speakers_data
            ]
            possible_file_names = [
                ", ".join(permutation)
                for permutation in permutations([speaker_name] + co_speakers_names)
            ]

        for video_file in files:
            video_file_lower = video_file.lower()

            for possible_file_name in possible_file_names:
                if possible_file_name in video_file_lower:
                    return video_file

        return ""

    def _get_speakers_data_for_events(self, events):
        all_users_ids = list(
            events.filter(submission__isnull=False).values_list(
                "submission__speaker_id", flat=True
            )
        ) + list(
            events.filter(additional_speakers__user_id__isnull=False).values_list(
                "additional_speakers__user_id", flat=True
            )
        )
        return get_users_data_by_ids(all_users_ids)


def walk_conference_videos_folder(storage, base_path):
    folders, files = storage.listdir(base_path)
    all_files = [f"{base_path}{file_}" for file_ in files]

    for folder in folders:
        if not folder:
            continue

        new_path = str(Path(base_path, folder)) + "/"
        all_files.extend(walk_conference_videos_folder(storage, new_path))

    return all_files


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass


@admin.register(AudienceLevel)
class AudienceLevelAdmin(admin.ModelAdmin):
    pass


@admin.register(Deadline)
class DeadlineAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Info", {"fields": ("name", "description", "type", "conference")}),
        ("Dates", {"fields": ("start", "end")}),
    )


class KeynoteSpeakerForm(forms.ModelForm):
    class Meta:
        model = KeynoteSpeaker
        fields = (
            "keynote",
            "user_id",
        )
        widgets = {
            "user_id": UsersBackendAutocomplete(admin.site),
        }


class KeynoteSpeakerInline(OrderedStackedInline):
    model = KeynoteSpeaker
    form = KeynoteSpeakerForm
    extra = 1
    fields = (
        "keynote",
        "user_id",
        "order",
        "move_up_down_links",
    )
    readonly_fields = (
        "order",
        "move_up_down_links",
    )
    extra = 1
    ordering = ("order",)


@admin.register(Keynote)
class KeynoteAdmin(OrderedInlineModelAdminMixin, OrderedModelAdmin):
    list_display = (
        "title",
        "conference",
        "move_up_down_links",
    )
    list_filter = ("conference",)
    fieldsets = (
        (
            _("Keynote"),
            {
                "fields": (
                    "conference",
                    "slug",
                    "title",
                    "description",
                    "topic",
                    "published",
                )
            },
        ),
    )
    inlines = [
        KeynoteSpeakerInline,
    ]

    def get_queryset(self, request):
        return Keynote.all_objects.all()


@admin.action(description="Send voucher via email")
def send_voucher_via_email(modeladmin, request, queryset):
    is_filtered_by_conference = (
        queryset.values_list("conference_id").distinct().count() == 1
    )

    if not is_filtered_by_conference:
        messages.error(request, "Please select only one conference")
        return

    count = 0
    for speaker_voucher in queryset.filter(pretix_voucher_id__isnull=False):
        send_speaker_voucher_email(speaker_voucher)
        count = count + 1

    messages.success(request, f"{count} Voucher emails scheduled!")


@admin.action(description="Create speaker vouchers on Pretix")
def create_speaker_vouchers_on_pretix(modeladmin, request, queryset):
    is_filtered_by_conference = (
        queryset.values_list("conference_id").distinct().count() == 1
    )

    if not is_filtered_by_conference:
        messages.error(request, "Please select only one conference")
        return

    conference = queryset.only("conference_id").first().conference

    if not conference.pretix_speaker_voucher_quota_id:
        messages.error(
            request,
            "Please configure the speaker voucher quota ID in the conference settings",
        )
        return

    count = 0

    for speaker_voucher in queryset.filter(pretix_voucher_id__isnull=True):
        if speaker_voucher.voucher_type == SpeakerVoucher.VoucherType.SPEAKER:
            price_mode = "set"
            value = "0.00"
        elif speaker_voucher.voucher_type == SpeakerVoucher.VoucherType.CO_SPEAKER:
            price_mode = "percent"
            value = "25.00"

        pretix_voucher = create_voucher(
            conference=speaker_voucher.conference,
            code=speaker_voucher.voucher_code,
            comment=f"Voucher for user_id={speaker_voucher.user_id}",
            tag="speakers",
            quota_id=speaker_voucher.conference.pretix_speaker_voucher_quota_id,
            price_mode=price_mode,
            value=value,
        )

        pretix_voucher_id = pretix_voucher["id"]
        speaker_voucher.pretix_voucher_id = pretix_voucher_id
        speaker_voucher.save()
        count = count + 1

    messages.success(request, f"{count} Vouchers created on Pretix!")


class SpeakerVoucherForm(forms.ModelForm):
    class Meta:
        model = SpeakerVoucher
        widgets = {
            "user_id": UsersBackendAutocomplete(admin.site),
        }
        fields = [
            "conference",
            "user_id",
            "voucher_type",
            "voucher_code",
            "pretix_voucher_id",
            "voucher_email_sent_at",
        ]


@admin.register(SpeakerVoucher)
class SpeakerVoucherAdmin(AdminUsersMixin, SearchUsersMixin):
    form = SpeakerVoucherForm
    search_fields = ("voucher_code",)
    list_filter = (
        "conference",
        "voucher_type",
        ("pretix_voucher_id", admin.EmptyFieldListFilter),
    )
    list_display = (
        "conference",
        "user_display_name",
        "voucher_type",
        "voucher_code",
        "created_on_pretix",
        "voucher_email_sent_at",
        "created",
    )
    user_fk = "user_id"
    actions = [
        create_speaker_vouchers_on_pretix,
        send_voucher_via_email,
    ]

    @admin.display(
        boolean=True,
    )
    def created_on_pretix(self, obj):
        return obj.pretix_voucher_id is not None

    def get_changeform_initial_data(self, request):
        return {"voucher_code": SpeakerVoucher.generate_code()}

    def user_display_name(self, obj):
        return self.get_user_display_name(obj.user_id)

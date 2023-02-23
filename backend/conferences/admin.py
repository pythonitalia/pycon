from django import forms
from django.contrib import admin, messages
from django.core import exceptions
from django.forms import BaseInlineFormSet
from django.forms.models import ModelForm
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from ordered_model.admin import (
    OrderedInlineModelAdminMixin,
    OrderedModelAdmin,
    OrderedStackedInline,
    OrderedTabularInline,
)

from conferences.models import SpeakerVoucher
from domain_events.publisher import send_speaker_voucher_email
from pretix import create_voucher
from sponsors.models import SponsorLevel
from users.autocomplete import UsersBackendAutocomplete
from users.mixins import AdminUsersMixin
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
                    "slack_new_speaker_invitation_answer_incoming_incoming_webhook_url",
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
        speaker_voucher.voucher_email_sent_at = timezone.now()
        speaker_voucher.save()
        count = count + 1

    messages.success(request, f"{count} Voucher emails sent!")


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
        pretix_voucher = create_voucher(
            conference=speaker_voucher.conference,
            code=speaker_voucher.voucher_code,
            comment=f"Voucher for user_id={speaker_voucher.user_id}",
            tag="speakers",
            quota_id=speaker_voucher.conference.pretix_speaker_voucher_quota_id,
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
            "voucher_code",
            "pretix_voucher_id",
            "voucher_email_sent_at",
        ]


@admin.register(SpeakerVoucher)
class SpeakerVoucherAdmin(AdminUsersMixin):
    form = SpeakerVoucherForm
    list_filter = ("conference", ("pretix_voucher_id", admin.EmptyFieldListFilter))
    list_display = (
        "conference",
        "user_display_name",
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

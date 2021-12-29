from django.contrib import admin
from django.core import exceptions
from django.forms import BaseInlineFormSet
from django.forms.models import ModelForm
from django.utils.translation import gettext_lazy as _

from sponsors.models import SponsorLevel

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


class SponsorLevelInline(admin.TabularInline):
    model = SponsorLevel


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
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
            "Hotel",
            {
                "fields": (
                    "pretix_hotel_ticket_id",
                    "pretix_hotel_room_type_question_id",
                    "pretix_hotel_checkin_question_id",
                    "pretix_hotel_checkout_question_id",
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
    )
    inlines = [DeadlineInline, DurationInline, SponsorLevelInline]


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


class KeynoteSpeakerInline(admin.StackedInline):
    model = KeynoteSpeaker
    extra = 1


@admin.register(Keynote)
class KeynoteAdmin(admin.ModelAdmin):
    list_display = (
        "keynote_title",
        "conference",
    )
    list_filter = ("conference",)
    fieldsets = (
        (
            _("Keynote"),
            {
                "fields": (
                    "conference",
                    "keynote_title",
                    "keynote_description",
                    "highlight_color",
                )
            },
        ),
    )
    inlines = [
        KeynoteSpeakerInline,
    ]

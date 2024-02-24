from custom_admin.admin import validate_single_conference_selection
from import_export.resources import ModelResource

from django import forms
from django.contrib import admin, messages
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from import_export.admin import ExportMixin
from import_export.fields import Field

from participants.models import Participant
from submissions.tasks import (
    send_proposal_rejected_email,
    send_proposal_in_waiting_list_email,
)
from users.admin_mixins import ConferencePermissionMixin


from .models import Submission, SubmissionComment, SubmissionTag, SubmissionType

EXPORT_SUBMISSION_FIELDS = (
    "id",
    "status",
    "pending_status",
    "languages",
    "title_en",
    "title_it",
    "elevator_pitch_it",
    "elevator_pitch_en",
    "abstract_it",
    "abstract_en",
    "notes",
    "tags",
    "audience_level",
    "type",
    "speaker_name",
    "speaker_email",
    "speaker_country",
    "speaker_gender",
)


class SubmissionResource(ModelResource):
    search_field = "speaker_id"
    title_en = Field()
    title_it = Field()
    elevator_pitch_en = Field()
    elevator_pitch_it = Field()
    abstract_en = Field()
    abstract_it = Field()
    speaker_name = Field()
    speaker_email = Field()
    speaker_country = Field()
    speaker_gender = Field()

    def dehydrate_title_en(self, obj: Submission):
        en = obj.title.data.get("en")
        return en if en else ""

    def dehydrate_title_it(self, obj: Submission):
        it = obj.title.data.get("it")
        return it if it else ""

    def dehydrate_elevator_pitch_en(self, obj: Submission):
        en = obj.elevator_pitch.data.get("en")
        return en if en else ""

    def dehydrate_elevator_pitch_it(self, obj: Submission):
        it = obj.elevator_pitch.data.get("it")
        return it if it else ""

    def dehydrate_abstract_en(self, obj: Submission):
        en = obj.abstract.data.get("en")
        return en if en else ""

    def dehydrate_abstract_it(self, obj: Submission):
        it = obj.abstract.data.get("it")
        return it if it else ""

    def dehydrate_tags(self, obj: Submission):
        return ", ".join([tag.name for tag in obj.tags.all()])

    def dehydrate_audience_level(self, obj: Submission):
        return obj.audience_level.name

    def dehydrate_type(self, obj: Submission):
        return obj.type.name

    def dehydrate_languages(self, obj: Submission):
        return ", ".join([lang.name for lang in obj.languages.all()])

    def dehydrate_speaker_name(self, obj: Submission):
        return obj.speaker.display_name

    def dehydrate_speaker_email(self, obj: Submission):
        return obj.speaker.email

    def dehydrate_speaker_country(self, obj: Submission):
        return obj.speaker.country

    def dehydrate_speaker_gender(self, obj: Submission):
        return obj.speaker.gender

    class Meta:
        model = Submission
        fields = EXPORT_SUBMISSION_FIELDS
        export_order = EXPORT_SUBMISSION_FIELDS


class SubmissionAdminForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = [
            "title",
            "slug",
            "speaker",
            "status",
            "type",
            "duration",
            "topic",
            "conference",
            "audience_level",
            "languages",
            "elevator_pitch",
            "abstract",
            "notes",
            "tags",
            "speaker_level",
            "previous_talk_video",
            "short_social_summary",
        ]


@admin.action(description="Move to waiting list")
@validate_single_conference_selection
def move_to_waiting_list(modeladmin, request, queryset):
    update_count = queryset.update(status=Submission.STATUS.waiting_list)
    messages.add_message(
        request, messages.INFO, f"Moved {update_count} proposals to the waiting list"
    )


@admin.action(description="Move to rejected")
@validate_single_conference_selection
def move_to_rejected(modeladmin, request, queryset):
    update_count = queryset.update(status=Submission.STATUS.rejected)
    messages.add_message(
        request, messages.INFO, f"Moved {update_count} proposals to rejected"
    )


@admin.action(description="Send proposal rejected email")
@validate_single_conference_selection
def send_proposal_rejected_email_action(modeladmin, request, queryset):
    for proposal in queryset.filter(status=Submission.STATUS.rejected):
        send_proposal_rejected_email.delay(proposal.id)

    messages.add_message(
        request,
        messages.INFO,
        f"Scheduled rejection emails to {queryset.count()} proposals",
    )


@admin.action(description="Send proposal in waiting list email")
@validate_single_conference_selection
def send_proposal_in_waiting_list_email_action(modeladmin, request, queryset):
    for proposal in queryset.filter(status=Submission.STATUS.waiting_list):
        send_proposal_in_waiting_list_email.delay(proposal.id)

    messages.add_message(
        request,
        messages.INFO,
        f"Scheduled waiting list emails to {queryset.count()} proposals",
    )


@admin.register(Submission)
class SubmissionAdmin(ExportMixin, ConferencePermissionMixin, admin.ModelAdmin):
    resource_class = SubmissionResource
    form = SubmissionAdminForm
    list_display = (
        "title",
        "speaker_display_name",
        "type",
        "status",
        "conference",
        "open_submission",
        "inline_tags",
        "duration",
        "audience_level",
        "created",
        "modified",
    )
    readonly_fields = ("created", "modified")
    fieldsets = (
        (
            _("Submission"),
            {
                "fields": (
                    "title",
                    "slug",
                    "speaker",
                    "status",
                    "created",
                    "modified",
                    "type",
                    "duration",
                    "tags",
                    "conference",
                    "audience_level",
                    "languages",
                )
            },
        ),
        (_("Details"), {"fields": ("elevator_pitch", "abstract", "notes")}),
        (_("Social"), {"fields": ("short_social_summary",)}),
    )
    list_filter = ("conference", "status", "pending_status", "type", "tags")
    search_fields = (
        "title",
        "elevator_pitch",
        "abstract",
        "notes",
        "previous_talk_video",
        "speaker__email",
        "speaker__full_name",
    )
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    user_fk = "speaker_id"
    actions = [
        move_to_waiting_list,
        move_to_rejected,
        send_proposal_rejected_email_action,
        send_proposal_in_waiting_list_email_action,
    ]
    autocomplete_fields = ("speaker",)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        submission = self.model.objects.get(id=object_id)
        owner_id = submission.speaker_id
        extra_context["participant"] = Participant.objects.filter(
            user_id=owner_id,
            conference_id=submission.conference_id,
        ).first()

        return super().change_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
        )

    @admin.display(
        description="Speaker",
    )
    def speaker_display_name(self, obj):
        return obj.speaker.display_name

    @admin.display(
        description="Tags",
    )
    def inline_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

    @admin.display(
        description="Open",
    )
    def open_submission(self, obj):  # pragma: no cover
        return mark_safe(
            f"""
                <a class="button" href="https://www.pycon.it/submission/{obj.hashid}"
                    target="_blank">Open</a>&nbsp;
            """
        )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    class Media:
        js = ["admin/js/jquery.init.js"]


@admin.register(SubmissionType)
class SubmissionTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(SubmissionTag)
class SubmissionTagAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(SubmissionComment)
class SubmissionCommentAdmin(admin.ModelAdmin):
    list_display = ("submission", "author", "text")

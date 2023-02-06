from django import forms
from django.contrib import admin
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from import_export.admin import ExportMixin
from import_export.fields import Field

from participants.models import Participant
from users.autocomplete import UsersBackendAutocomplete
from users.mixins import AdminUsersMixin, ResourceUsersByIdsMixin, SearchUsersMixin

from .models import Submission, SubmissionComment, SubmissionTag, SubmissionType

EXPORT_SUBMISSION_FIELDS = (
    "id",
    "languages",
    "title_en",
    "title_it",
    "status",
    "tags",
    "audience_level",
    "type",
)


class SubmissionResource(ResourceUsersByIdsMixin):
    search_field = "speaker_id"
    title_en = Field()
    title_it = Field()
    speaker_name = Field()
    speaker_email = Field()

    def dehydrate_title_en(self, obj: Submission):
        en = obj.title.data.get("en")
        return en if en else ""

    def dehydrate_title_it(self, obj: Submission):
        it = obj.title.data.get("it")
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
        return self.get_user_display_name(obj.speaker_id)

    def dehydrate_speaker_email(self, obj: Submission):
        user_data = self.get_user_data(obj.speaker_id)
        return user_data["email"]

    class Meta:
        model = Submission
        fields = EXPORT_SUBMISSION_FIELDS
        export_order = EXPORT_SUBMISSION_FIELDS


class SubmissionCommentInlineForm(forms.ModelForm):
    class Meta:
        model = SubmissionComment
        fields = ["submission", "author_id", "text"]
        widgets = {
            "author_id": UsersBackendAutocomplete(admin.site),
        }


class SubmissionCommentInline(admin.TabularInline):
    model = SubmissionComment
    form = SubmissionCommentInlineForm


class SubmissionAdminForm(forms.ModelForm):
    class Meta:
        model = Submission
        widgets = {
            "speaker_id": UsersBackendAutocomplete(admin.site),
        }
        fields = [
            "title",
            "slug",
            "speaker_id",
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
        ]


@admin.register(Submission)
class SubmissionAdmin(ExportMixin, AdminUsersMixin, SearchUsersMixin):
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
                    "speaker_id",
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
    )
    list_filter = ("conference", "status", "pending_status", "type", "tags")
    search_fields = (
        "title",
        "elevator_pitch",
        "abstract",
        "notes",
        "previous_talk_video",
    )
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    inlines = [SubmissionCommentInline]
    user_fk = "speaker_id"

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
        return self.get_user_display_name(obj.speaker_id)

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
    list_display = ("submission", "author_id", "text")

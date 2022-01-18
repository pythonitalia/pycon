from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from users.autocomplete import UsersBackendAutocomplete
from users.mixins import AdminUsersMixin

from .models import Submission, SubmissionComment, SubmissionTag, SubmissionType


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
class SubmissionAdmin(AdminUsersMixin):
    form = SubmissionAdminForm
    list_display = (
        "title",
        "speaker_display_name",
        "type",
        "status",
        "conference",
        "topic",
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
                    "topic",
                    "conference",
                    "audience_level",
                    "languages",
                )
            },
        ),
        (_("Details"), {"fields": ("elevator_pitch", "abstract", "notes", "tags")}),
        (_("Speaker"), {"fields": ("speaker_level", "previous_talk_video")}),
    )
    list_filter = ("conference", "type", "topic", "status")
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

    def speaker_display_name(self, obj):
        return self.get_user_display_name(obj.speaker_id)

    speaker_display_name.short_description = "Speaker"

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

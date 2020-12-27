from dal_admin_filters import AutocompleteFilter
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Submission, SubmissionComment, SubmissionTag, SubmissionType


class SpeakerFilter(AutocompleteFilter):
    title = "Speaker"
    field_name = "speaker"
    autocomplete_url = "user-autocomplete"


class SubmissionCommentInline(admin.TabularInline):
    model = SubmissionComment


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "speaker_name",
        "type",
        "status",
        "conference",
        "topic",
        "duration",
        "audience_level",
    )
    fieldsets = (
        (
            _("Submission"),
            {
                "fields": (
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
                )
            },
        ),
        (_("Details"), {"fields": ("elevator_pitch", "abstract", "notes", "tags")}),
        (_("Speaker"), {"fields": ("speaker_level", "previous_talk_video")}),
    )
    list_filter = ("conference", "type", "topic", "status", SpeakerFilter)
    search_fields = ("title", "abstract")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    inlines = [SubmissionCommentInline]

    def speaker_name(self, obj):
        return obj.speaker.full_name or obj.speaker.name or obj.speaker.email

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

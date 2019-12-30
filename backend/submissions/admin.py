from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Submission, SubmissionTag, SubmissionType, SubmissionComment


class SubmissionCommentInline(admin.TabularInline):
    model = SubmissionComment


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "conference", "topic", "audience_level")
    fieldsets = (
        (
            _("Submission"),
            {
                "fields": (
                    "title",
                    "slug",
                    "speaker",
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
    list_filter = ("conference", "type", "topic")
    search_fields = ("title", "abstract")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    inlines = [SubmissionCommentInline]


@admin.register(SubmissionType)
class SubmissionTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(SubmissionTag)
class SubmissionTagAdmin(admin.ModelAdmin):
    list_display = ("name",)

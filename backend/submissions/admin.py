from django.contrib import admin

from .models import Submission, SubmissionTag, SubmissionType


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "conference", "topic", "audience_level")
    fieldsets = (
        (
            "Submission",
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
        ("Details", {"fields": ("elevator_pitch", "abstract", "notes")}),
    )
    list_filter = ("conference", "type", "topic")
    search_fields = ("title", "abstract")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(SubmissionType)
class SubmissionTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(SubmissionTag)
class SubmissionTagAdmin(admin.ModelAdmin):
    list_display = ("name",)

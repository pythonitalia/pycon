from django.contrib import admin

from .models import Submission, SubmissionType


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "conference", "topic", "audience_level")
    fieldsets = (
        (
            "Submission",
            {
                "fields": (
                    "title",
                    "type",
                    "conference",
                    "topic",
                    "audience_level",
                    "languages",
                )
            },
        ),
    )
    list_filter = ("conference", "type", "topic")
    search_fields = ("title", "abstract")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(SubmissionType)
class SubmissionTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)

from django.contrib import admin

from .models import Submission, SubmissionType


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "type",
        "conference",
        "topic",
        "language",
        "audience_level",
    )
    list_filter = ("conference", "type", "topic")
    search_fields = ("title", "abstract")


@admin.register(SubmissionType)
class SubmissionTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)

from django.contrib import admin

from .models import (
    AudienceLevel,
    Conference,
    Deadline,
    Duration,
    TicketFare,
    TicketFareQuestion,
    Topic,
)


class DeadlineInline(admin.TabularInline):
    model = Deadline


class DurationInline(admin.StackedInline):
    model = Duration
    filter_horizontal = ("allowed_submission_types",)


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
    inlines = [DeadlineInline, DurationInline]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass


@admin.register(AudienceLevel)
class AudienceLevelAdmin(admin.ModelAdmin):
    pass


class TicketFareQuestionInline(admin.StackedInline):
    model = TicketFareQuestion


@admin.register(TicketFare)
class TicketFareAdmin(admin.ModelAdmin):
    list_display = ("conference", "name")
    list_filter = ("conference", "questions")
    inlines = [TicketFareQuestionInline]

    fieldsets = (
        ("Info", {"fields": ("conference", "name", "code", "price", "description")}),
        ("Deadline", {"fields": ("start", "end")}),
    )


@admin.register(Deadline)
class DeadlineAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Info", {"fields": ("name", "description", "type", "conference")}),
        ("Dates", {"fields": ("start", "end")}),
    )

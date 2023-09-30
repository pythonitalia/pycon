from dal_admin_filters import AutocompleteFilter
from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from import_export.admin import ExportMixin
from import_export.fields import Field
from import_export.resources import ModelResource
from import_export.widgets import DecimalWidget

from voting.models import RankRequest, RankStat, RankSubmission, Vote


class SubmissionFilter(AutocompleteFilter):
    title = "Submission"
    field_name = "submission"
    autocomplete_url = "submission-autocomplete"


class ConferenceFilter(AutocompleteFilter):
    title = "Conference"
    field_name = "submission__conference"
    autocomplete_url = "submission-conference-autocomplete"


class VoteAdminForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ["value", "user", "submission"]


class VoteResource(ModelResource):
    class Meta:
        model = Vote
        fields = (
            "id",
            "value",
            "user",
            "submission",
            "submission__conference__code",
        )


@admin.register(Vote)
class VoteAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = VoteResource
    form = VoteAdminForm
    readonly_fields = ("created", "modified")
    list_display = ("submission", "user_display_name", "value", "created", "modified")
    list_filter = ("submission__conference", SubmissionFilter, "value")
    search_fields = (
        "submission__title",
        "user__email",
    )

    user_fk = "user_id"

    @admin.display(
        description="User",
    )
    def user_display_name(self, obj):
        return obj.user.display_name

    class Media:
        js = ["admin/js/jquery.init.js"]


EXPORT_RANK_SUBMISSION_FIELDS = (
    "tag__name",
    "rank",
    "score",
    "submission__id",
    "submission__hashid",
    "submission__audience_level__name",
    "submission__type__name",
    "submission__duration__name",
    "submission__language",
    "vote_count",
    "tags",
    "submission__speaker_id",
    "full_name",
    "gender",
    "rank_request__conference__code",
)


class RankSubmissionResource(ModelResource):
    conference_filter_by = "rank_request__conference"
    submission__hashid = Field()
    submission__title = Field()
    submission__language = Field()
    gender = Field()
    full_name = Field()
    tags = Field()
    vote_count = Field()

    score = Field(column_name="score", attribute="score", widget=DecimalWidget())

    def dehydrate_submission__hashid(self, obj):
        return obj.submission.hashid

    def dehydrate_submission__title(self, obj):
        return obj.submission.title.localize("en")

    def dehydrate_submission__language(self, obj):
        return ", ".join([lang.code for lang in obj.submission.languages.all()])

    def dehydrate_gender(self, obj):
        return obj.submission.speaker.gender

    def dehydrate_full_name(self, obj):
        return obj.submission.speaker.display_name

    def dehydrate_tags(self, obj):
        return "\n".join([t.name for t in obj.submission.tags.all()])

    def dehydrate_vote_count(self, obj):
        return Vote.objects.filter(submission=obj.submission).count()

    class Meta:
        model = RankSubmission
        fields = EXPORT_RANK_SUBMISSION_FIELDS
        export_order = EXPORT_RANK_SUBMISSION_FIELDS


@admin.register(RankSubmission)
class RankSubmissionAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = RankSubmissionResource
    list_display = (
        "tag",
        "position",
        "score",
        "title",
        "type",
        "duration",
        "tags",
        "topic",
        "level",
        "language",
        "speaker",
        "gender",
        "view_submission",
    )
    ordering = (
        "tag",
        "rank",
        "-score",
    )
    list_filter = (
        "rank_request_id",
        "submission__type",
        "tag",
        "submission__topic",
        "submission__duration",
    )

    def title(self, obj):
        return obj.submission.title

    def type(self, obj):
        return obj.submission.type

    def topic(self, obj):
        return obj.submission.topic.name if obj.submission.topic else ""

    def level(self, obj):
        return obj.submission.audience_level.name

    def duration(self, obj):
        return obj.submission.duration.duration

    def language(self, obj):
        emoji = {"it": "🇮🇹", "en": "🇬🇧"}
        langs = [emoji[lang.code] for lang in obj.submission.languages.all()]
        return " ".join(langs)

    def speaker(self, obj):
        return obj.submission.speaker.display_name

    @admin.display(
        description="Gender",
    )
    def gender(self, obj):
        emoji = {
            "": "",
            "male": "👨🏻‍💻",
            "female": "👩🏼‍💻",
            "other": "🧑🏻‍🎤",
            "not_say": "⛔️",
        }

        speaker_gender = obj.submission.speaker.gender
        return emoji[speaker_gender]

    def tags(self, obj):
        tags = [tag.name for tag in obj.submission.tags.all()]
        return ", ".join(tags)

    @admin.display(
        description="Rank",
    )
    def position(self, obj):
        return f"{obj.rank} / {obj.total_submissions_per_tag}"

    @admin.display(
        description="View",
    )
    def view_submission(self, obj):  # pragma: no cover
        return format_html(
            '<a class="button" href="{url}">Open</a>&nbsp;',
            url=reverse(
                "admin:submissions_submission_change",
                kwargs={"object_id": obj.submission.id},
            ),
        )


@admin.register(RankRequest)
class RankRequestAdmin(admin.ModelAdmin):
    list_display = ("conference", "created", "is_public", "view_rank")

    @admin.display(
        description="View",
    )
    def view_rank(self, obj):
        return format_html(
            '<a class="button" '
            'href="{url}?'
            f'rank_request_id__id__exact={obj.id}">Open</a>&nbsp;',
            url=reverse("admin:voting_ranksubmission_changelist"),
        )


@admin.register(RankStat)
class RankStatAdmin(admin.ModelAdmin):
    list_filter = ("rank_request__conference",)

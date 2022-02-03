from dal_admin_filters import AutocompleteFilter
from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from import_export.admin import ExportMixin
from import_export.fields import Field
from import_export.resources import ModelResource
from import_export.widgets import DecimalWidget

from users.autocomplete import UsersBackendAutocomplete
from users.mixins import AdminUsersMixin, ResourceUsersMixin
from voting.models import RankRequest, RankSubmission, Vote


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
        widgets = {
            "user_id": UsersBackendAutocomplete(admin.site),
        }
        fields = ["value", "user_id", "submission"]


class VoteResource(ModelResource):
    class Meta:
        model = Vote
        fields = (
            "id",
            "value",
            "user_id",
            "submission",
            "submission__conference__code",
        )


@admin.register(Vote)
class VoteAdmin(ExportMixin, AdminUsersMixin):
    resource_class = VoteResource
    form = VoteAdminForm
    readonly_fields = ("created", "modified")
    list_display = ("submission", "user_display_name", "value", "created", "modified")
    list_filter = ("submission__conference", SubmissionFilter, "value")
    search_fields = (
        "submission__title",
        "user_id",
    )

    user_fk = "user_id"

    def user_display_name(self, obj):
        return self.get_user_display_name(obj.user_id)

    user_display_name.short_description = "User"

    class Media:
        js = ["admin/js/jquery.init.js"]


EXPORT_RANK_SUBMISSION_FIELDS = (
    "absolute_rank",
    "absolute_score",
    "submission__topic__name",
    "topic_rank",
    "submission__id",
    "submission__hashid",
    "submission__title",
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


class RankSubmissionResource(ResourceUsersMixin):
    conference_filter_by = "rank_request__conference"
    user_fk = "submission__speaker_id"
    submission__hashid = Field()
    submission__language = Field()
    gender = Field()
    full_name = Field()
    tags = Field()
    vote_count = Field()

    absolute_score = Field(
        column_name="absolute_score", attribute="absolute_score", widget=DecimalWidget()
    )

    def dehydrate_submission__hashid(self, obj):
        return obj.submission.hashid

    def dehydrate_submission__language(self, obj):
        return [lang.code for lang in obj.submission.languages.all()]

    def dehydrate_gender(self, obj):
        return self.get_user_data(obj.submission.speaker_id)["gender"]

    def dehydrate_full_name(self, obj):
        return self.get_user_display_name(obj.submission.speaker_id)

    def dehydrate_tags(self, obj):
        return [t.name for t in obj.submission.tags.all()]

    def dehydrate_vote_count(self, obj):
        return Vote.objects.filter(submission=obj.submission).count()

    class Meta:
        model = RankSubmission
        fields = EXPORT_RANK_SUBMISSION_FIELDS
        export_order = EXPORT_RANK_SUBMISSION_FIELDS


@admin.register(RankSubmission)
class RankSubmissionAdmin(ExportMixin, AdminUsersMixin):
    resource_class = RankSubmissionResource
    user_fk = "submission__speaker_id"
    list_display = (
        "absolute_rank",
        "absolute_score",
        "duration",
        "title",
        "type",
        "topic",
        "topic_rank",
        "level",
        "language",
        "speaker",
        "gender",
        "view_submission",
    )
    ordering = ("absolute_rank",)
    list_filter = (
        "rank_request_id",
        "submission__type",
        "submission__topic",
        "submission__duration",
    )

    def title(self, obj):
        return obj.submission.title

    def type(self, obj):
        return obj.submission.type

    def topic(self, obj):
        return obj.submission.topic.name

    def level(self, obj):
        return obj.submission.audience_level.name

    def duration(self, obj):
        return obj.submission.duration.duration

    def language(self, obj):
        emoji = {"it": "🇮🇹", "en": "🇬🇧"}
        langs = [emoji[lang.code] for lang in obj.submission.languages.all()]
        return " ".join(langs)

    def speaker(self, obj):
        return self.get_user_display_name(obj.submission.speaker_id)

    def gender(self, obj):
        emoji = {
            "": "",
            "male": "👨🏻‍💻",
            "female": "👩🏼‍💻",
            "other": "🧑🏻‍🎤",
            "not_say": "⛔️",
        }

        speaker_gender = self.get_user_data(obj.submission.speaker_id)["gender"]
        return emoji[speaker_gender]

    gender.short_description = "Gender"

    def view_submission(self, obj):  # pragma: no cover
        return format_html(
            '<a class="button" href="{url}">Open</a>&nbsp;',
            url=reverse(
                "admin:submissions_submission_change",
                kwargs={"object_id": obj.submission.id},
            ),
        )

    view_submission.short_description = "View"
    view_submission.allow_tags = True


@admin.register(RankRequest)
class RankRequestAdmin(admin.ModelAdmin):
    list_display = ("conference", "created", "view_rank")

    def view_rank(self, obj):
        return format_html(
            '<a class="button" '
            'href="{url}?'
            f'rank_request_id__id__exact={obj.id}">Open</a>&nbsp;',
            url=reverse("admin:voting_ranksubmission_changelist"),
        )

    view_rank.short_description = "View"
    view_rank.allow_tags = True

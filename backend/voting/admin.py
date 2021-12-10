from dal_admin_filters import AutocompleteFilter
from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from users.autocomplete import UsersBackendAutocomplete
from users.mixins import AdminUsersMixin
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


@admin.register(Vote)
class VoteAdmin(AdminUsersMixin):
    form = VoteAdminForm
    list_display = ("submission", "user_display_name", "value")
    list_filter = (SubmissionFilter, "value")
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


@admin.register(RankSubmission)
class RankSubmissionAdmin(AdminUsersMixin):
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

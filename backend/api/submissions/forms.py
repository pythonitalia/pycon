from django import forms
from django.core import exceptions
from django.utils.translation import gettext_lazy as _

from api.forms import ContextAwareModelForm, HashidModelChoiceField
from conferences.models import AudienceLevel, Conference
from domain_events.publisher import notify_new_submission
from languages.models import Language
from notifications.aws import send_comment_notification
from submissions.models import Submission, SubmissionComment, SubmissionTag


class SendSubmissionCommentForm(ContextAwareModelForm):
    submission = HashidModelChoiceField(queryset=Submission.objects.all())

    def save(self, commit=True):
        self.instance.author_id = self.context.request.user.id
        comment = super().save(commit=commit)

        send_comment_notification(comment)

        return comment

    class Meta:
        model = SubmissionComment
        fields = ("text", "submission")


class SubmissionForm(ContextAwareModelForm):
    languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(), to_field_name="code"
    )

    audience_level = forms.ModelChoiceField(
        queryset=AudienceLevel.objects.all(), to_field_name="id"
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=SubmissionTag.objects.all(), to_field_name="id", required=False
    )

    def clean(self):
        cleaned_data = super().clean()

        conference = cleaned_data.get("conference", None)

        if not conference and self.instance:
            conference = self.instance.conference

        languages = cleaned_data.get("languages", None)

        if languages:
            for language in languages.all():
                if not conference.languages.filter(id=language.id).exists():
                    raise exceptions.ValidationError(
                        {
                            "languages": _("%(language)s is not an allowed language")
                            % {"language": str(language)}
                        }
                    )

        return cleaned_data


class UpdateSubmissionForm(SubmissionForm):
    instance = forms.ModelChoiceField(
        queryset=Submission.objects.all(), to_field_name="id"
    )

    @classmethod
    def get_instance(cls, hashid):
        return Submission.objects.get_by_hashid(hashid)

    def clean(self):
        cleaned_data = super().clean()

        if not self.instance.can_edit(self.context.request):
            raise exceptions.ValidationError(_("You cannot edit this submission"))

        return cleaned_data

    def save(self, commit=True):
        return super().save(commit=commit)

    class Meta:
        model = Submission
        fields = (
            "instance",
            "title",
            "abstract",
            "topic",
            "languages",
            "type",
            "duration",
            "elevator_pitch",
            "notes",
            "audience_level",
            "tags",
            "speaker_level",
            "previous_talk_video",
        )


class SendSubmissionForm(SubmissionForm):
    conference = forms.ModelChoiceField(
        queryset=Conference.objects.all(), to_field_name="code", required=True
    )

    def clean(self):
        cleaned_data = super().clean()

        conference = cleaned_data.get("conference", None)

        if not conference.is_cfp_open:
            raise forms.ValidationError(_("The call for paper is not open!"))

    def save(self, commit=True):
        request = self.context.request
        self.instance.speaker_id = request.user.id
        instance = super().save(commit=commit)
        notify_new_submission(
            submission_id=instance.id,
            title=instance.title,
            elevator_pitch=instance.elevator_pitch,
            submission_type=instance.type.name,
            admin_url=request.build_absolute_uri(instance.get_admin_url()),
            duration=instance.duration.duration,
            topic=instance.topic.name,
            author_id=instance.author_id,
        )
        return instance

    class Meta:
        model = Submission
        fields = (
            "title",
            "abstract",
            "topic",
            "languages",
            "conference",
            "type",
            "duration",
            "elevator_pitch",
            "notes",
            "audience_level",
            "tags",
            "speaker_level",
            "previous_talk_video",
        )

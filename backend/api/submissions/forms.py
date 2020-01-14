from api.forms import ContextAwareModelForm
from conferences.models import AudienceLevel, Conference
from django import forms
from django.core import exceptions
from django.utils.translation import ugettext_lazy as _
from integrations.tasks import notify_new_submission
from languages.models import Language
from submissions.models import Submission, SubmissionTag


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

        if not self.instance.can_edit(self.context["request"]):
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
        request = self.context["request"]
        self.instance.speaker = request.user
        instance = super().save(commit=commit)
        notify_new_submission(
            instance.title,
            instance.elevator_pitch,
            instance.type.name,
            request.build_absolute_uri(instance.get_admin_url()),
            instance.duration.duration,
            instance.topic.name,
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

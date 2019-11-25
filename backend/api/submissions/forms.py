from django import forms
from django.core import exceptions
from django.utils.translation import ugettext_lazy as _

from api.forms import ContextAwareModelForm
from conferences.models import AudienceLevel, Conference
from integrations.tasks import notify_new_submission
from languages.models import Language
from submissions.models import Submission


class SendSubmissionForm(ContextAwareModelForm):
    conference = forms.ModelChoiceField(
        queryset=Conference.objects.all(), to_field_name="code"
    )
    languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(), to_field_name="code"
    )
    audience_level = forms.ModelChoiceField(
        queryset=AudienceLevel.objects.all(), to_field_name="id"
    )

    def clean(self):
        cleaned_data = super().clean()
        conference = cleaned_data.get("conference")

        if conference and not conference.is_cfp_open:
            raise forms.ValidationError(_("The call for papers is not open!"))

        if cleaned_data.get("languages"):
            for language in cleaned_data["languages"].all():
                if not conference.languages.filter(id=language.id).exists():
                    raise exceptions.ValidationError(
                        {
                            "languages": _("%(language)s is not an allowed language")
                            % {"language": str(language)}
                        }
                    )

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
        )

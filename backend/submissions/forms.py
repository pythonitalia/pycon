from django import forms

from django.utils.translation import ugettext_lazy as _

from api.forms import ContextAwareForm
from languages.models import Language
from conferences.models import Conference, AudienceLevel

from .models import Submission


class SendSubmissionForm(ContextAwareForm):
    conference = forms.ModelChoiceField(queryset=Conference.objects.all(), to_field_name='code', required=True)
    language = forms.ModelChoiceField(queryset=Language.objects.all(), to_field_name='code', required=True)
    audience_level = forms.ModelChoiceField(
        queryset=AudienceLevel.objects.all(), to_field_name='name',
        required=True)

    def clean(self):
        cleaned_data = super().clean()
        conference = cleaned_data.get('conference')

        if conference and not conference.is_cfp_open:
            raise forms.ValidationError(_('The call for papers is not open!'))

    def save(self, commit=True):
        self.instance.speaker = self.context.user
        return super().save(commit=commit)

    class Meta:
        model = Submission
        fields = (
            'title',
            'abstract',
            'topic',
            'language',
            'conference',
            'type',
            'duration',
            'elevator_pitch',
            'notes',
            'audience_level',
        )

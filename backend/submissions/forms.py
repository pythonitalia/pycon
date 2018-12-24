from django import forms

from django.utils.translation import ugettext_lazy as _

from api.forms import GrapheneModelForm
from languages.models import Language
from conferences.models import Conference

from .models import Submission


class SendSubmissionForm(GrapheneModelForm):
    conference = forms.ModelChoiceField(queryset=Conference.objects.all(), to_field_name='code', required=True)
    language = forms.ModelChoiceField(queryset=Language.objects.all(), to_field_name='code', required=True)

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
        fields = ('title', 'abstract', 'topic', 'language', 'conference', 'type')

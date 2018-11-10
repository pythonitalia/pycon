from django import forms

from api.forms import GrapheneModelForm
from languages.models import Language
from conferences.models import Conference

from .models import Talk


class ProposeTalkForm(GrapheneModelForm):
    conference = forms.ModelChoiceField(queryset=Conference.objects.all(), to_field_name='code')
    language = forms.ModelChoiceField(queryset=Language.objects.all(), to_field_name='code')

    def save(self, commit=True):
        self.instance.owner = self.context.user
        return super().save(commit=commit)

    class Meta:
        model = Talk
        fields = ('title', 'abstract', 'topic', 'language', 'conference')

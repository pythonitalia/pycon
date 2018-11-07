from django import forms

from languages.models import Language

from .models import Talk


class ProposeTalkForm(forms.ModelForm):
    language = forms.ModelChoiceField(queryset=Language.objects.all(), to_field_name='code')

    class Meta:
        model = Talk
        fields = ('title', 'abstract', 'topic', 'language', 'conference')

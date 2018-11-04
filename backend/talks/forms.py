from django import forms

from .models import Talk


class ProposeTalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = ('title', 'abstract', 'track', 'language', 'conference')

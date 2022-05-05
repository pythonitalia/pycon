from django import forms

from conferences.models import Conference


class EmailSpeakersForm(forms.Form):
    conference = forms.ModelChoiceField(queryset=Conference.objects.all())
    subject = forms.CharField()
    body = forms.CharField(widget=forms.Textarea(attrs={"rows": 20, "cols": 50}))

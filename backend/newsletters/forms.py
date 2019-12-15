from django import forms


class SendEmailForm(forms.Form):
    subject = forms.CharField(label="Subject", max_length=100)
    body = forms.CharField(label="Body", widget=forms.Textarea)

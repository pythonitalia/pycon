from django import forms
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices

from .models import Subscription

RECIPIENTS_TYPES = Choices(
    ("newsletter", _("Newsletter")),
    # ("other", _("Other")),
)


class SendEmailForm(forms.Form):
    subject = forms.CharField(label="Subject", max_length=100)
    body = forms.CharField(label="Body", widget=forms.Textarea)
    recipients_types = forms.ChoiceField(
        label="Recipients Type", choices=RECIPIENTS_TYPES
    )

    def clean_recipients_types(self):
        # if self.cleaned_data["recipients_types"] == "newsletter":
        recipients = [subscription.email for subscription in Subscription.objects.all()]
        self.cleaned_data["recipients"] = recipients

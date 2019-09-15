from api.forms import ContextAwareModelForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from voting.models import Vote

from .fields import VoteValueField


class SendVoteForm(ContextAwareModelForm):
    value = VoteValueField()

    def clean(self):
        cleaned_data = super().clean()
        submission = cleaned_data.get("submission")

        if submission.conference and not submission.conference.is_voting_open:
            raise forms.ValidationError(_("The voting session is not open!"))

    def save(self, commit=True):
        request = self.context["request"]

        submission = self.cleaned_data.get("submission")

        try:
            self.instance = Vote.objects.get(user=request.user, submission=submission)
        except Vote.DoesNotExist:
            pass

        self.instance.user = request.user
        self.instance.value = self.cleaned_data["value"]
        return super().save(commit=commit)

    class Meta:
        model = Vote
        fields = ("submission", "value")

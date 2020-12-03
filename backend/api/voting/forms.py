from api.forms import ContextAwareModelForm, HashidModelChoiceField
from django import forms
from django.utils.translation import ugettext_lazy as _
from submissions.models import Submission
from voting.models import Vote

from .fields import VoteValueField


class SendVoteForm(ContextAwareModelForm):
    value = VoteValueField()
    submission = HashidModelChoiceField(queryset=Submission.objects.all())

    def clean(self):
        cleaned_data = super().clean()
        submission = cleaned_data.get("submission")

        if submission.conference and not submission.conference.is_voting_open:
            raise forms.ValidationError(_("The voting session is not open!"))

        logged_user = self.context.request.user

        if not logged_user.can_vote(submission.conference):
            raise forms.ValidationError(_("You cannot vote without a ticket"))

    def save(self, commit=True):
        request = self.context.request

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

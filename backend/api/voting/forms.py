from django import forms
from django.utils.translation import gettext_lazy as _

from api.forms import ContextAwareModelForm, HashidModelChoiceField
from submissions.models import Submission
from voting.helpers import pastaporto_user_info_can_vote
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

        pastaporto = self.context.request.pastaporto

        if not pastaporto_user_info_can_vote(pastaporto, submission.conference):
            raise forms.ValidationError(_("You cannot vote without a ticket"))

    def save(self, commit=True):
        request = self.context.request

        submission = self.cleaned_data.get("submission")

        try:
            self.instance = Vote.objects.get(
                user_id=request.user.id, submission=submission
            )
        except Vote.DoesNotExist:
            pass

        self.instance.user_id = request.user.id
        self.instance.value = self.cleaned_data["value"]
        return super().save(commit=commit)

    class Meta:
        model = Vote
        fields = ("submission", "value")

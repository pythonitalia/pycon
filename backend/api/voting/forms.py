from api.forms import ContextAwareModelForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from pretix.db import user_has_admission_ticket
from submissions.models import Submission
from voting.models import Vote
from api.forms import HashidModelChoiceField
from .fields import VoteValueField


class SendVoteForm(ContextAwareModelForm):
    value = VoteValueField()
    submission = HashidModelChoiceField(queryset=Submission.objects.all())

    def clean(self):
        cleaned_data = super().clean()
        submission = cleaned_data.get("submission")

        if submission.conference and not submission.conference.is_voting_open:
            raise forms.ValidationError(_("The voting session is not open!"))

        logged_user = self.context["request"].user

        if not user_has_admission_ticket(
            logged_user.email, submission.conference.pretix_event_id
        ):
            raise forms.ValidationError(_("You cannot vote without a ticket"))

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

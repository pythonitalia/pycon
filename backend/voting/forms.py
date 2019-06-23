from django import forms
from django.utils.translation import ugettext_lazy as _

from api.forms import ContextAwareForm
from voting.models import Vote


class SendVoteForm(ContextAwareForm):

    def clean(self):
        cleaned_data = super().clean()
        submission = cleaned_data.get('submission')

        if submission.conference and not submission.conference.is_voting_open:
            raise forms.ValidationError(_('The voting session is not open!'))

    def save(self, commit=True):
        return super().save(commit=commit)

    class Meta:
        model = Vote
        fields = (
            'submission',
            'value',
            'user',
            'range'
        )

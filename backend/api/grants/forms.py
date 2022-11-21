from django import forms
from django.core import exceptions
from django.utils.translation import gettext_lazy as _

from api.forms import ContextAwareModelForm
from conferences.models import Conference
from grants.models import Grant


class GrantForm(ContextAwareModelForm):
    conference = forms.ModelChoiceField(
        queryset=Conference.objects.all(), to_field_name="code", required=True
    )

    def clean(self):
        cleaned_data = super().clean()

        conference = cleaned_data.get("conference", None)

        if not conference and self.instance:
            conference = self.instance.conference

        if not conference.is_grants_open:
            raise exceptions.ValidationError(_("The grants form is now closed!"))

        if Grant.objects.filter(user_id=self.context.request.user.id).exists():
            raise exceptions.ValidationError(_("Grant already submitted!"))

    def save(self, commit=True):
        self.instance.user_id = self.context.request.user.id

        return super().save(commit=commit)

    class Meta:
        model = Grant
        fields = (
            "name",
            "full_name",
            "conference",
            "age",
            "gender",
            "occupation",
            "grant_type",
            "python_usage",
            "been_to_other_events",
            "interested_in_volunteering",
            "needs_funds_for_travel",
            "why",
            "notes",
            "travelling_from",
        )

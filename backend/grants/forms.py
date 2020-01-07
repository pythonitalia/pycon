from api.forms import ContextAwareModelForm
from conferences.models import Conference
from django import forms

from .models import Grant


class GrantForm(ContextAwareModelForm):
    conference = forms.ModelChoiceField(
        queryset=Conference.objects.all(), to_field_name="code", required=True
    )

    class Meta:
        model = Grant
        fields = (
            "name",
            "full_name",
            "conference",
            "email",
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

from django import forms
from django.contrib import admin
from badges.models import AttendeeConferenceRole
from badges.roles import Role


class AttendeeConferenceRoleForm(forms.ModelForm):
    roles = forms.MultipleChoiceField(
        choices=Role.choices(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = AttendeeConferenceRole
        fields = [
            "conference",
            "order_position_id",
            "user",
            "roles",
        ]


@admin.register(AttendeeConferenceRole)
class AttendeeConferenceRoleAdmin(admin.ModelAdmin):
    list_display = ("user", "order_position_id", "conference", "roles")
    list_filter = (
        "conference",
        "roles",
    )
    form = AttendeeConferenceRoleForm
    user_fk = "user_id"

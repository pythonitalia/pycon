from django import forms
from django.contrib import admin
from badges.models import AttendeeConferenceRole
from badges.roles import Role
from users.mixins import AdminUsersMixin
from users.autocomplete import UsersBackendAutocomplete


class AttendeeConferenceRoleForm(forms.ModelForm):
    roles = forms.MultipleChoiceField(
        choices=Role.choices(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = AttendeeConferenceRole
        widgets = {
            "user_id": UsersBackendAutocomplete(admin.site),
        }
        fields = [
            "conference",
            "order_position_id",
            "user_id",
            "roles",
        ]


@admin.register(AttendeeConferenceRole)
class AttendeeConferenceRoleAdmin(AdminUsersMixin):
    form = AttendeeConferenceRoleForm
    user_fk = "user_id"

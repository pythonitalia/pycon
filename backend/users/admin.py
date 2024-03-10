from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import User


class PyConUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    class Meta:
        model = User
        fields = ("email",)


class PyConUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    class Meta:
        model = User
        fields = "__all__"


@admin.register(User)
class PyConUserAdmin(UserAdmin):
    # The forms to add and change user instances

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "email",
                    "password",
                    "name",
                    "full_name",
                    "gender",
                    "date_birth",
                    "open_to_recruiting",
                    "open_to_newsletter",
                    "user_hashid",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "admin_all_conferences",
                    "admin_conferences",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )
    filter_horizontal = (
        "groups",
        "user_permissions",
        "admin_conferences",
    )

    form = PyConUserChangeForm
    add_form = PyConUserCreationForm
    readonly_fields = ("date_joined", "user_hashid")
    list_display = ("email", "full_name", "is_staff", "is_superuser")
    search_fields = ("email",)
    ordering = ("email",)

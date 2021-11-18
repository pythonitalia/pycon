from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.db.models import Q
from django.urls import path
from django.utils.translation import gettext_lazy as _

from .admin_views import users_autocomplete
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
                )
            },
        ),
        (_("Address"), {"fields": ("country",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )

    form = PyConUserChangeForm
    add_form = PyConUserCreationForm
    readonly_fields = ("date_joined",)
    list_display = ("email", "full_name", "is_staff", "is_superuser")
    search_fields = ("email",)
    ordering = ("email",)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .filter(Q(is_staff=True) | Q(is_superuser=True))
        )

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "users-autocomplete/",
                self.admin_site.admin_view(users_autocomplete),
                name="users-admin-autocomplete",
            ),
        ]
        return my_urls + urls


admin.site.register(User, PyConUserAdmin)

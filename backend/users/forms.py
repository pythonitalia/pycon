from django.contrib.auth import authenticate, login
from django.forms import CharField, EmailField, ValidationError
from django.utils.translation import ugettext_lazy as _
from strawberry_forms.forms import FormWithContext

from .models import User


class LoginForm(FormWithContext):
    email = EmailField()
    password = CharField()

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        user = authenticate(email=email, password=password)

        if not user or not user.is_active:
            raise ValidationError(_("Wrong email/password combination"))

        cleaned_data["user"] = user
        return cleaned_data

    def save(self):
        user = self.cleaned_data.get("user")
        login(self.context["request"], user)
        return user


class RegisterForm(FormWithContext):
    email = EmailField()
    password = CharField()

    def clean(self):
        cleaned_data = super().clean()

        email = self.cleaned_data.get("email")

        try:
            User.objects.get(email=email)

            raise ValidationError(
                {"email": _("This email is already used by another account")}
            )
        except User.DoesNotExist:
            pass

        return cleaned_data

    def save(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        user = User.objects.create_user(email=email, password=password)
        user = authenticate(email=email, password=password)
        login(self.context["request"], user)
        return user

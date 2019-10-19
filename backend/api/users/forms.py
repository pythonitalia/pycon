import os

from django.contrib.auth import authenticate, login
from django.core import exceptions
from django.core.files.storage import default_storage
from django.forms import BooleanField, CharField, EmailField, ValidationError
from django.utils.translation import ugettext_lazy as _

from api.forms import ContextAwareModelForm
from strawberry_forms.forms import FormWithContext
from users.models import User


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


class UpdateUserForm(ContextAwareModelForm):
    date_birth = CharField(required=False)
    open_to_recruiting = BooleanField(required=False)
    open_to_newsletter = BooleanField(required=False)
    country = CharField(required=False)
    image = CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()

        image = self.cleaned_data.get("image")
        if image:
            if not default_storage.exists(image):
                name = os.path.basename(image)
                raise exceptions.ValidationError(
                    {"image": _(f"File '{name}' not found")}
                )

        return cleaned_data

    def save(self, commit=True):
        user = self.context["request"].user

        try:
            self.instance = User.objects.get(id=user.id)
        except User.DoesNotExist:
            pass

        for key, value in self.cleaned_data.items():
            setattr(self.instance, key, value)

        image = self.cleaned_data.get("image")
        if image:
            file = default_storage.open(image)
            self.instance.image.save(os.path.basename(image), file)
            default_storage.delete(image)

        return super().save(commit=commit)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "gender")

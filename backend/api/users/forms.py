from base64 import urlsafe_b64decode

from api.forms import ContextAwareModelForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.forms import BooleanField, CharField, EmailField, ValidationError
from django.utils.translation import ugettext_lazy as _
from newsletters.models import Subscription
from notifications.emails import send_request_password_reset_mail
from strawberry_forms.forms import FormWithContext
from users.models import User


class ResetPasswordForm(FormWithContext):
    token = CharField()
    encoded_user_id = CharField()
    password = CharField()

    def clean(self):
        cleaned_data = super().clean()

        token = cleaned_data["token"]
        userid = urlsafe_b64decode(cleaned_data["encoded_user_id"])

        user = User.objects.filter(id=userid).first()

        if not user:
            raise ValidationError({"encoded_user_id": _("Invalid user")})

        if not default_token_generator.check_token(user, token):
            raise ValidationError({"token": _("Invalid token")})

        cleaned_data["user"] = user
        return cleaned_data

    def save(self):
        new_password = self.cleaned_data["password"]
        user = self.cleaned_data["user"]

        user.set_password(new_password)
        user.save()
        return True


class RequestPasswordResetForm(FormWithContext):
    email = EmailField()

    def save(self):
        user = User.objects.filter(email=self.cleaned_data["email"]).first()

        if not user:
            return True

        token = default_token_generator.make_token(user)
        return send_request_password_reset_mail(user, token) == 1


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
        login(self.context.request, user)
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
        login(self.context.request, user)
        return user


class UpdateUserForm(ContextAwareModelForm):
    date_birth = CharField(required=False)
    open_to_recruiting = BooleanField(required=False)
    open_to_newsletter = BooleanField(required=False)
    country = CharField(required=False)
    image = CharField(required=False)

    def save(self, commit=True):
        user = self.context.request.user

        self.instance = User.objects.get(id=user.id)

        for key, value in self.cleaned_data.items():
            setattr(self.instance, key, value)

        if self.cleaned_data.get("open_to_newsletter"):
            Subscription.objects.get_or_create(email=user.email)
        else:
            try:
                Subscription.objects.get(email=user.email).delete()
            except Subscription.DoesNotExist:
                pass
        return super().save(commit=commit)

    class Meta:
        model = User
        fields = ("name", "full_name", "gender")


class LogoutForm(FormWithContext):
    def save(self):
        logout(self.context.request)
        return True

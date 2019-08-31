from api.forms import ContextAwareModelForm
from django.contrib.auth import authenticate, login
from django.forms import BooleanField, CharField, EmailField, ValidationError
from django.utils.translation import ugettext_lazy as _
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
    # TODO: Why if I tell you required=FALSE, the mutation fail if I don't put
    # Bool! (instead of 'Bool')?
    open_to_recruiting = BooleanField(required=False)
    open_to_newsletter = BooleanField(required=False)
    country = CharField(required=False)

    def clean(self):

        if not self.context.user.is_authenticated:
            raise ValidationError(_("Must authenticate to update User information"))

        return super().clean()

    def save(self, commit=True):
        super().save(commit=commit)
        return User.objects.get(id=self.context.user.id)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "gender",
            "business_name",
            "fiscal_code",
            "vat_number",
            "phone_number",
            "recipient_code",
            "pec_address",
            "address",
        )


class UpdateImageForm(FormWithContext):
    url = CharField()

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self):

        user = self.context.user

        user.image = self.cleaned_data.get("url")
        user.save()

        return user

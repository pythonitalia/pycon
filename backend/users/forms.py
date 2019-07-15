from django.contrib.auth import authenticate, login
from django.forms import Form, CharField, EmailField
from django.utils.translation import ugettext_lazy as _

from graphene_form.forms import FormWithContext

from .types import MeUserType, EmailPasswordCombinationError, EmailAlreadyUsedError
from .models import User


class LoginForm(FormWithContext):
    email = EmailField()
    password = CharField()

    def save(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        user = authenticate(email=email, password=password)

        if not user or not user.is_active:
            return EmailPasswordCombinationError(_('Wrong email/password combination'))

        login(self.context, user)
        return user


class RegisterForm(FormWithContext):
    email = EmailField()
    password = CharField()

    def save(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        try:
            User.objects.get(email=email)
            return EmailAlreadyUsedError(_('This email is already used by another account'))
        except User.DoesNotExist:
            pass

        user = User.objects.create_user(email=email, password=password)
        # TODO: Improve
        user = authenticate(email=email, password=password)
        login(self.context, user)
        return user

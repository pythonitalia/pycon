from django.contrib.auth import authenticate, login
from django.forms import Form, CharField
from django.utils.translation import ugettext_lazy as _

from graphene_form.forms import FormWithContext

from .types import MeUserType, EmailPasswordCombinationError


class LoginForm(FormWithContext):
    email = CharField()
    password = CharField()

    def save(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        user = authenticate(email=email, password=password)

        if not user or not user.is_active:
            return EmailPasswordCombinationError(_('Wrong email/password combination'))

        login(self.context, user)
        return user

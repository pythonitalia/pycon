from graphene import ObjectType

from graphene_form.mutations import FormMutation

from .types import EmailPasswordCombinationError, MeUserType, EmailAlreadyUsedError
from .forms import LoginForm, RegisterForm


class Login(FormMutation):
    class Meta:
        form_class = LoginForm
        output_types = (
            EmailPasswordCombinationError,
            MeUserType,
        )


class Register(FormMutation):
    class Meta:
        form_class = RegisterForm
        output_types = (
            MeUserType,
            EmailAlreadyUsedError,
        )

class UsersMutations(ObjectType):
    login = Login.Field()
    register = Register.Field()

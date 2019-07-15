from graphene import ObjectType

from graphene_form.mutations import FormMutation

from .types import EmailPasswordCombinationError, MeUserType
from .forms import LoginForm


class Login(FormMutation):
    class Meta:
        form_class = LoginForm
        output_types = (
            EmailPasswordCombinationError,
            MeUserType,
        )


class UsersMutations(ObjectType):
    login = Login.Field()

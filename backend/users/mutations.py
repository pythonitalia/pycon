from strawberry_forms.mutations import FormMutation

from .forms import LoginForm, RegisterForm
from .types import MeUserType


class Login(FormMutation):
    @classmethod
    def transform(cls, result):
        return MeUserType(id=result.id, email=result.email)

    class Meta:
        form_class = LoginForm
        output_types = (MeUserType,)


class Register(FormMutation):
    @classmethod
    def transform(cls, result):
        return MeUserType(id=result.id, email=result.email)

    class Meta:
        form_class = RegisterForm
        output_types = (MeUserType,)


class UsersMutations:
    login = Login.Mutation
    register = Register.Mutation

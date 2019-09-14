from strawberry_forms.mutations import FormMutation

from .forms import LoginForm, RegisterForm
from .types import MeUser


class Login(FormMutation):
    @classmethod
    def transform(cls, result):
        return MeUser(id=result.id, email=result.email)

    class Meta:
        form_class = LoginForm
        output_types = (MeUser,)


class Register(FormMutation):
    @classmethod
    def transform(cls, result):
        return MeUser(id=result.id, email=result.email)

    class Meta:
        form_class = RegisterForm
        output_types = (MeUser,)


class UsersMutations:
    login = Login.Mutation
    register = Register.Mutation

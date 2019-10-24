from api.submissions.permissions import IsAuthenticated
from strawberry_forms.mutations import FormMutation

from .forms import LoginForm, RegisterForm, UpdateUserForm
from .types import MeUser


class BaseUserMutation(FormMutation):
    @classmethod
    def transform(cls, result):
        return MeUser(
            id=result.id,
            email=result.email,
            first_name=result.first_name,
            last_name=result.last_name,
            gender=result.gender,
            open_to_recruiting=result.open_to_recruiting,
            open_to_newsletter=result.open_to_newsletter,
            date_birth=result.date_birth,
            country=result.country,
        )

    class Meta:

        form_class = RegisterForm
        output_types = (MeUser,)


class Login(BaseUserMutation):
    class Meta:
        form_class = LoginForm
        output_types = (MeUser,)


class Register(BaseUserMutation):
    class Meta:
        form_class = RegisterForm
        output_types = (MeUser,)


class Update(BaseUserMutation):
    class Meta:
        form_class = UpdateUserForm
        output_types = (MeUser,)
        permission_classes = (IsAuthenticated,)


class UsersMutations:
    login = Login.Mutation
    register = Register.Mutation
    update = Update.Mutation

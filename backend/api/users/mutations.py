from api.submissions.permissions import IsAuthenticated
from strawberry_forms.mutations import FormMutation

from ..types import OperationResult
from .forms import (
    LoginForm,
    RegisterForm,
    RequestPasswordResetForm,
    ResetPasswordForm,
    UpdateUserForm,
)
from .types import MeUser


class BaseUserMutation(FormMutation):
    @classmethod
    def transform(cls, result):
        return MeUser(
            id=result.id,
            email=result.email,
            name=result.name,
            full_name=result.full_name,
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


class RequestPasswordResetMutation(FormMutation):
    @classmethod
    def transform(cls, result):
        return OperationResult(ok=result)

    class Meta:
        form_class = RequestPasswordResetForm
        output_types = (OperationResult,)


class ResetPasswordMutation(FormMutation):
    @classmethod
    def transform(cls, result):
        return OperationResult(ok=result)

    class Meta:
        form_class = ResetPasswordForm
        output_types = (OperationResult,)


class UsersMutations:
    login = Login.Mutation
    register = Register.Mutation
    update = Update.Mutation
    request_password_reset = RequestPasswordResetMutation.Mutation
    reset_password = ResetPasswordMutation.Mutation

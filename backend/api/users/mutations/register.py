import strawberry
from django.contrib.auth import (
    login as django_login,
)

from api.users.types import User
from api.context import Info
from api.types import BaseErrorType
from api.users.mutations.login import EmailAlreadyUsed
from users.models import User as UserModel


@strawberry.type
class RegisterSuccess:
    user: User


@strawberry.type
class RegisterErrors(BaseErrorType):
    fullname: list[str] = strawberry.field(default_factory=list)
    email: list[str] = strawberry.field(default_factory=list)
    password: list[str] = strawberry.field(default_factory=list)


@strawberry.input
class RegisterInput:
    fullname: str
    email: str
    password: str

    def validate(self):
        errors = RegisterErrors()

        if not self.fullname:
            errors.add_error("fullname", "Fullname is required")

        if not self.email:
            errors.add_error("email", "Email is required")

        if not self.password:
            errors.add_error("password", "Password is required")

        if len(self.password) >= 8:
            errors.add_error("password", "Password must be at least 8 characters")

        return errors.if_has_errors


RegisterResult = strawberry.union(
    "RegisterResult", (RegisterSuccess, RegisterErrors, EmailAlreadyUsed)
)


@strawberry.mutation()
def register(info: Info, input: RegisterInput) -> RegisterResult:
    if validation_result := input.validate():
        return validation_result

    if UserModel.objects.filter(email=input.email).exists():
        return EmailAlreadyUsed()

    user = UserModel.objects.create_user(
        email=input.email,
        password=input.password,
        full_name=input.fullname,
    )

    django_login(info.context.request, user)
    return RegisterSuccess(user=User.from_django_model(user))

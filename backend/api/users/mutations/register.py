from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import strawberry
from django.contrib.auth import (
    authenticate,
    login as django_login,
)

from api.users.types import User
from api.context import Info
from api.types import BaseErrorType
from users.models import User as UserModel
from typing import Annotated, Union


@strawberry.type
class EmailAlreadyUsed:
    message: str = "Email already used"


@strawberry.type
class RegisterSuccess:
    user: User


@strawberry.type
class RegisterErrors(BaseErrorType):
    @strawberry.type
    class _RegisterErrors:
        fullname: list[str] = strawberry.field(default_factory=list)
        email: list[str] = strawberry.field(default_factory=list)
        password: list[str] = strawberry.field(default_factory=list)

    errors: _RegisterErrors = None


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
        else:
            try:
                validate_email(self.email)
            except ValidationError:
                errors.add_error("email", "Email is not valid")

        if not self.password:
            errors.add_error("password", "Password is required")

        if self.password and len(self.password) < 8:
            errors.add_error("password", "Password must be at least 8 characters")

        return errors.if_has_errors


RegisterResult = Annotated[
    Union[RegisterSuccess, RegisterErrors, EmailAlreadyUsed],
    strawberry.union(name="RegisterResult"),
]


@strawberry.mutation()
def register(info: Info, input: RegisterInput) -> RegisterResult:
    if validation_result := input.validate():
        return validation_result

    user_email = UserModel.objects.normalize_email(input.email)
    if UserModel.objects.filter(email=user_email).exists():
        return EmailAlreadyUsed()

    user = UserModel.objects.create_user(
        email=input.email,
        password=input.password,
        full_name=input.fullname,
    )
    user = authenticate(email=user_email, password=input.password)
    if not user:
        raise Exception("Something went wrong")

    django_login(info.context.request, user)
    return RegisterSuccess(user=User.from_django_model(user))

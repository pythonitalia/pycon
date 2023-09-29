import logging
from typing import Optional
import strawberry
from django.contrib.auth import (
    authenticate,
    login as django_login,
)

from api.users.types import User
from api.context import Info
from api.types import BaseErrorType

logger = logging.getLogger(__file__)


@strawberry.type
class LoginSuccess:
    user: User


@strawberry.type
class WrongEmailOrPassword:
    message: str = "Invalid username/password combination"


@strawberry.type
class LoginErrors(BaseErrorType):
    @strawberry.type
    class _LoginErrors:
        email: list[str] = strawberry.field(default_factory=list)
        password: list[str] = strawberry.field(default_factory=list)

    _error_class = _LoginErrors
    errors: Optional[_LoginErrors] = None


@strawberry.input
class LoginInput:
    email: str
    password: str

    def validate(self):
        errors = LoginErrors()

        if not self.email:
            errors.add_error("email", "Email is required")

        if not self.password:
            errors.add_error("password", "Password is required")

        return errors.if_has_errors


@strawberry.type
class EmailAlreadyUsed:
    message: str = "Email already used"


LoginResult = strawberry.union(
    "LoginResult", (LoginSuccess, LoginErrors, WrongEmailOrPassword)
)


@strawberry.mutation()
def login(info: Info, input: LoginInput) -> LoginResult:
    if validation_result := input.validate():
        return validation_result

    logger.info("Login attempt for email=%s", input.email)

    email = input.email
    password = input.password

    user = authenticate(email=email, password=password)

    if not user or not user.is_active:
        return WrongEmailOrPassword()

    django_login(info.context.request, user)
    logger.info("Login completed with success for email=%s", input.email)
    return LoginSuccess(user=User.from_django_model(user))

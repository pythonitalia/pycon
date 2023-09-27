from strawberry.tools import create_type
import strawberry
from django.contrib.auth import (
    authenticate,
    login as django_login,
)

from api.users.types import User
from api.context import Info


@strawberry.type
class LoginSuccess:
    user: User


@strawberry.type
class WrongEmailOrPassword:
    message: str = "Invalid username/password combination"


@strawberry.input
class LoginInput:
    email: str
    password: str


LoginResult = strawberry.union("LoginResult", (LoginSuccess, WrongEmailOrPassword))


def login(info: Info, input: LoginInput) -> LoginResult:
    email = input.email
    password = input.password

    user = authenticate(email=email, password=password)

    if not user or not user.is_active:
        return WrongEmailOrPassword()

    django_login(info.context.request, user)
    return LoginSuccess(user=User.from_django_model(user))


LoginMutation = create_type(
    "LoginMutation",
    [
        login,
    ],
)

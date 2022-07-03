from __future__ import annotations

import pydantic
import strawberry
from pythonit_toolkit.api.builder import create_validation_error_type
from pythonit_toolkit.api.types import PydanticError

from users.api.context import Info
from users.api.types import User
from users.domain import entities, services
from users.domain.services import LoginInputModel
from users.domain.services.exceptions import (
    UserIsNotActiveError,
    WrongEmailOrPasswordError,
)


@strawberry.experimental.pydantic.input(LoginInputModel, fields=["email", "password"])
class LoginInput:
    pass


@strawberry.type
class LoginSuccess:
    user: User

    @classmethod
    def from_domain(cls, user: entities.User) -> LoginSuccess:
        return cls(user=User.from_domain(user))


@strawberry.type
class WrongEmailOrPassword:
    message: str = "Invalid username/password combination"


@strawberry.type
class LoginErrors:
    email: PydanticError = None
    password: PydanticError = None


LoginValidationError = create_validation_error_type("Login", LoginErrors)


LoginResult = strawberry.union(
    "LoginResult", (LoginSuccess, WrongEmailOrPassword, LoginValidationError)
)


@strawberry.mutation
async def login(info: Info, input: LoginInput) -> LoginResult:
    try:
        input_model = input.to_pydantic()
    except pydantic.ValidationError as exc:
        return LoginValidationError.from_validation_error(exc)

    try:
        user = await services.login(
            input_model, users_repository=info.context.users_repository
        )
    except (WrongEmailOrPasswordError, UserIsNotActiveError):
        return WrongEmailOrPassword()

    info.context._authenticated_as = user
    return LoginSuccess.from_domain(user)

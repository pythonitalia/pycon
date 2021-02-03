from __future__ import annotations

import pydantic
import strawberry

from users.api.builder import create_validation_error_type
from users.api.context import Info
from users.api.types import PydanticError, User
from users.domain import entities, services
from users.domain.services import LoginInputModel
from users.domain.services.exceptions import WrongUsernameOrPasswordError


@strawberry.experimental.pydantic.input(LoginInputModel, fields=["email", "password"])
class LoginInput:
    pass


@strawberry.type
class LoginSuccess:
    user: User
    token: str

    @classmethod
    def from_domain(cls, user: entities.User) -> LoginSuccess:
        return cls(user=User.from_domain(user), token=user.generate_token())


@strawberry.type
class WrongUsernameOrPassword:
    message: str = "Invalid username/password combination"


@strawberry.type
class LoginErrors:
    email: PydanticError = None
    password: PydanticError = None


LoginValidationError = create_validation_error_type("Login", LoginErrors)


LoginResult = strawberry.union(
    "LoginResult", (LoginSuccess, WrongUsernameOrPassword, LoginValidationError)
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
    except WrongUsernameOrPasswordError:
        return WrongUsernameOrPassword()

    return LoginSuccess.from_domain(user)

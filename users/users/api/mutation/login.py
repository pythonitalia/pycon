from __future__ import annotations

import pydantic
import strawberry

from users.api.context import Info
from users.api.types import PydanticError, User, ValidationError
from users.domain import entities, services
from users.domain.services import LoginInputModel
from users.domain.services.exceptions import UsernameOrPasswordInvalidError


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
class UsernameAndPasswordCombinationWrong:
    message: str = "Invalid username/password combination"


@strawberry.type(name="LoginErrors")
class LoginValidationError:
    email: PydanticError = None
    password: PydanticError = None


LoginResult = strawberry.union(
    "LoginResult",
    (
        LoginSuccess,
        UsernameAndPasswordCombinationWrong,
        ValidationError[LoginValidationError],
    ),
)


@strawberry.mutation
async def login(info: Info, input: LoginInput) -> LoginResult:
    try:
        input_model = input.to_pydantic()
    except pydantic.ValidationError as exc:
        return ValidationError.from_validation_error(exc, LoginValidationError)

    try:
        user = await services.login(
            input_model, users_repository=info.context.users_repository
        )
    except UsernameOrPasswordInvalidError:
        return UsernameAndPasswordCombinationWrong()

    return LoginSuccess.from_domain(user)

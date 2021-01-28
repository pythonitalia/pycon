from __future__ import annotations

import strawberry
from users.api.context import Info
from users.api.types import User
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


LoginResult = strawberry.union(
    "LoginResult", (LoginSuccess, UsernameAndPasswordCombinationWrong)
)


@strawberry.mutation
async def login(info: Info, input: LoginInput) -> LoginResult:
    input_model = input.to_pydantic()

    try:
        user = await services.login(
            input_model, users_repository=info.context.users_repository
        )
    except UsernameOrPasswordInvalidError:
        return UsernameAndPasswordCombinationWrong()

    return LoginSuccess.from_domain(user)

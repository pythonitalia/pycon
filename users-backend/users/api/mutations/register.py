from __future__ import annotations

import pydantic
import strawberry
from pythonit_toolkit.api.builder import create_validation_error_type
from pythonit_toolkit.api.types import PydanticError
from pythonit_toolkit.pastaporto.actions import create_user_auth_pastaporto_action

from users.api.context import Info
from users.api.types import User
from users.domain import entities, services
from users.domain.services import RegisterInputModel
from users.domain.services.exceptions import EmailAlreadyUsedError


@strawberry.experimental.pydantic.input(
    RegisterInputModel, fields=["email", "password"]
)
class RegisterInput:
    pass


@strawberry.type
class RegisterErrors:
    email: PydanticError = None
    password: PydanticError = None


RegisterValidationError = create_validation_error_type("Register", RegisterErrors)


@strawberry.type
class RegisterSuccess:
    user: User

    @classmethod
    def from_domain(cls, user: entities.User) -> RegisterSuccess:
        return cls(user=User.from_domain(user))


@strawberry.type
class EmailAlreadyUsed:
    message: str = "Email specified is already used"


RegisterResult = strawberry.union(
    "RegisterResult", (RegisterSuccess, EmailAlreadyUsed, RegisterValidationError)
)


@strawberry.mutation
async def register(info: Info, input: RegisterInput) -> RegisterResult:
    try:
        input_model = input.to_pydantic()
    except pydantic.ValidationError as exc:
        return RegisterValidationError.from_validation_error(exc)

    try:
        user = await services.register(
            input_model, users_repository=info.context.users_repository
        )
    except EmailAlreadyUsedError:
        return EmailAlreadyUsed()

    info.context.pastaporto_action = create_user_auth_pastaporto_action(user.id)
    return RegisterSuccess.from_domain(user)

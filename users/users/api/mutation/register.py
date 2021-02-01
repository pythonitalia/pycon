from __future__ import annotations

import pydantic
import strawberry

from users.api.builder import create_validation_error_type
from users.api.context import Info
from users.api.types import PydanticError, User
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
    token: str

    @classmethod
    def from_domain(cls, user: entities.User) -> RegisterSuccess:
        return cls(user=User.from_domain(user), token=user.generate_token())


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

    return RegisterSuccess.from_domain(user)

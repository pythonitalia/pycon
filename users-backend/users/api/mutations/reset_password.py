import pydantic
import strawberry
from pythonit_toolkit.api.builder import create_validation_error_type
from pythonit_toolkit.api.types import PydanticError

from users.api.context import Info
from users.api.types import OperationSuccess
from users.domain import services
from users.domain.services import ResetPasswordInput as ResetPasswordInputModel
from users.domain.services import exceptions


@strawberry.experimental.pydantic.input(
    ResetPasswordInputModel, fields=["token", "new_password"]
)
class ResetPasswordInput:
    pass


@strawberry.type
class ResetPasswordErrors:
    token: PydanticError = None
    new_password: PydanticError = None


@strawberry.type
class ResetPasswordTokenExpired:
    message: str = "Reset password token expired"


@strawberry.type
class ResetPasswordTokenInvalid:
    message: str = "Reset password token invalid"


ResetPasswordValidationError = create_validation_error_type(
    "ResetPassword", ResetPasswordErrors
)

ResetPasswordResult = strawberry.union(
    "ResetPasswordResult",
    (
        ResetPasswordValidationError,
        OperationSuccess,
        ResetPasswordTokenExpired,
        ResetPasswordTokenInvalid,
    ),
)


@strawberry.mutation
async def reset_password(info: Info, input: ResetPasswordInput) -> ResetPasswordResult:
    try:
        input_model = input.to_pydantic()
    except pydantic.ValidationError as exc:
        return ResetPasswordValidationError.from_validation_error(exc)

    try:
        await services.reset_password(
            input_model, repository=info.context.users_repository
        )
    except exceptions.ResetPasswordTokenExpiredError:
        return ResetPasswordTokenExpired()
    except (
        exceptions.ResetPasswordTokenInvalidError,
        exceptions.UserIsNotActiveError,
        exceptions.UserDoesNotExistError,
    ):
        return ResetPasswordTokenInvalid()

    return OperationSuccess(ok=True)

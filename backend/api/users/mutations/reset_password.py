from api.users.types import UserDoesNotExistError
from api.context import Info
from api.types import ErrorResult, OperationResult
import strawberry
from django.utils.translation import ugettext_lazy as _

from pydantic import ValidationError

from users.domain import services
from users.domain.services import exceptions


@strawberry.experimental.pydantic.input(
    services.ResetPasswordModel, fields=["token", "encoded_user_id", "password"]
)
class ResetPasswordInput:
    pass


@strawberry.experimental.pydantic.error_type(
    services.ResetPasswordModel, fields=["token", "encoded_user_id", "password"]
)
class ResetPasswordInputError:
    pass


@strawberry.type
class ResetPasswordTokenNotValidError(ErrorResult):
    def __init__(self) -> None:
        super().__init__(error_message=_("Reset password token not vaild/expired"))


ResetPasswordOutput = strawberry.union(
    "ResetPasswordOutput",
    (
        OperationResult,
        ResetPasswordInputError,
        UserDoesNotExistError,
        ResetPasswordTokenNotValidError,
    ),
)


@strawberry.mutation
def reset_password(info: Info, input: ResetPasswordInput) -> ResetPasswordOutput:
    try:
        model = input.to_pydantic()
    except ValidationError as exc:
        # TODO implement
        print("ValidationError:", exc)
        # return ResetPasswordInputError.from_pydantic_error(exc)
        return OperationResult(ok=False)

    try:
        services.reset_password(model, users_repository=info.context.users_repository)
    except exceptions.UserDoesNotExistError as exc:
        return UserDoesNotExistError()
    except exceptions.ResetPasswordTokenNotValidError as exc:
        return ResetPasswordTokenNotValidError()

    return OperationResult(ok=True)

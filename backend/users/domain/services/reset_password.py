from base64 import urlsafe_b64decode
from users.domain.services.exceptions import (
    ResetPasswordTokenNotValidError,
    UserDoesNotExistError,
)
from users.domain.repository import UsersRepository
from users.domain.entities import UserID

from pydantic import BaseModel, constr


class ResetPasswordModel(BaseModel):
    token: constr(min_length=1)
    encoded_user_id: constr(min_length=1)
    password: constr(min_length=1)

    @property
    def decoded_user_id(self) -> UserID:
        return urlsafe_b64decode(self.encoded_user_id)


def reset_password(
    input: ResetPasswordModel, *, users_repository: UsersRepository
) -> None:
    user = users_repository.get_by_id(input.decoded_user_id)

    if not user:
        raise UserDoesNotExistError()

    if not users_repository.validate_reset_password_token(user, input.token):
        raise ResetPasswordTokenNotValidError()

    user.set_password(input.password)
    users_repository.save_user(user)

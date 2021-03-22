import logging

import jwt
from pydantic import BaseModel, constr

from users.domain.repository import UsersRepository
from users.domain.services.exceptions import (
    ResetPasswordTokenExpiredError,
    ResetPasswordTokenInvalidError,
    UserDoesNotExistError,
    UserIsNotActiveError,
)
from users.settings import SECRET_KEY

logger = logging.getLogger(__name__)


class ResetPasswordInput(BaseModel):
    token: str
    new_password: constr(min_length=8)

    def decode_token(self) -> dict:
        return jwt.decode(
            self.token,
            str(SECRET_KEY),
            issuer="users",
            audience="users/reset-password",
            algorithms=["HS256"],
            options={"require": ["exp", "iss", "aud", "iat", "jti"]},
        )


async def reset_password(input: ResetPasswordInput, *, repository: UsersRepository):
    try:
        decoded_token = input.decode_token()
    except jwt.ExpiredSignatureError:
        raise ResetPasswordTokenExpiredError()
    except (jwt.InvalidAudienceError, jwt.MissingRequiredClaimError):
        raise ResetPasswordTokenInvalidError()

    user_id = decoded_token["user_id"]
    user = await repository.get_by_id(user_id)

    if not user:
        logger.error("Decoding reset password token return invalid user_id=%s", user_id)
        raise UserDoesNotExistError()

    if not user.is_active:
        logger.error("Trying to reset password of not active user_id=%s", user_id)
        raise UserIsNotActiveError()

    jti = decoded_token["jti"]

    if jti != user.get_reset_password_jwt_id():
        raise ResetPasswordTokenInvalidError()

    logger.info("Resetting password of user_id=%s", user_id)
    user.set_password(input.new_password)
    user.request_reset_password_id = user.request_reset_password_id + 1
    await repository.save_user(user)
    await repository.commit()

import logging

from users.domain.entities import User
from users.domain.services.exceptions import UserIsNotActiveError

logger = logging.getLogger(__file__)


async def request_reset_password(user: User):
    if not user.is_active:
        logger.info(
            "Trying to request reset password of not active user_id=%s", user.id
        )
        raise UserIsNotActiveError()

    token = user.create_reset_password_token()
    logger.info("Sending reset password token of user_id=%s", user.id)
    print("token", token)
    # send email
    pass

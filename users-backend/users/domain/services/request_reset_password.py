import logging

from pythonit_toolkit.emails.templates import EmailTemplate
from users.domain.entities import User
from users.domain.services.exceptions import UserIsNotActiveError
from users.emails import send_email
from users.settings import ASSOCIATION_FRONTEND_URL

logger = logging.getLogger(__file__)


async def request_reset_password(user: User):
    if not user.is_active:
        logger.info(
            "Trying to request reset password of not active user_id=%s", user.id
        )
        raise UserIsNotActiveError()

    token = user.create_reset_password_token()

    send_email(
        template=EmailTemplate.RESET_PASSWORD,
        to=user.email,
        subject="Reset your password",
        variables={
            "firstname": user.name,
            "resetpasswordlink": f"{ASSOCIATION_FRONTEND_URL}/reset-password/{token}",
        },
    )
    logger.info("Sent reset password token of user_id=%s", user.id)

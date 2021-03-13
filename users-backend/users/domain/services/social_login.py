import dataclasses
import logging
from datetime import datetime

from pydantic import BaseModel, EmailStr, constr

from users.domain.entities import UNUSABLE_PASSWORD, User
from users.domain.repository import AbstractUsersRepository

logger = logging.getLogger(__name__)


class SocialAccount(BaseModel):
    social_id: constr(min_length=1)
    fullname: str = ""
    first_name: str = ""
    middle_name: str = ""
    last_name: str = ""


class SocialLoginInput(BaseModel):
    email: EmailStr
    social_account: SocialAccount


async def social_login(
    input: SocialLoginInput, *, users_repository: AbstractUsersRepository
) -> User:
    logger.info(
        "Request social login with social_id=%s and google provider",
        input.social_account.social_id,
    )

    user = await users_repository.get_by_email(input.email)

    if not user:
        logger.info("Social login not found, creating a new user")

        user = await users_repository.create_user(
            User(
                email=input.email,
                password=UNUSABLE_PASSWORD,
                date_joined=datetime.utcnow(),
                fullname=input.social_account.fullname,
                name=input.social_account.first_name,
            )
        )
        user = dataclasses.replace(user, password=None)
        await users_repository.commit()

        logger.info("Created user %s for social login", user.id)
    else:
        logger.info("Found user %s for social login", user.id)

    return user

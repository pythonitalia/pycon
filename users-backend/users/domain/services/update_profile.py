import dataclasses
from datetime import date
from typing import Optional

from pydantic import BaseModel, constr

from users.domain.entities import User
from users.domain.repository import AbstractUsersRepository
from users.domain.services.exceptions import UserDoesNotExistError, UserIsNotActiveError


class UpdateProfileInput(BaseModel):
    name: constr(min_length=1)
    full_name: constr(min_length=1)
    gender: str
    open_to_recruiting: bool
    open_to_newsletter: bool
    country: str
    date_birth: Optional[date]
    tagline: str


async def update_profile(
    user_id: int,
    input: UpdateProfileInput,
    *,
    users_repository: AbstractUsersRepository
) -> User:
    user = await users_repository.get_by_id(user_id)

    if not user:
        raise UserDoesNotExistError()

    if not user.is_active:
        raise UserIsNotActiveError()

    user.name = input.name
    user.fullname = input.full_name
    user.gender = input.gender
    user.open_to_newsletter = input.open_to_newsletter
    user.open_to_recruiting = input.open_to_recruiting
    user.date_birth = input.date_birth
    user.country = input.country
    user.tagline = input.tagline

    await users_repository.save_user(user)
    updated_user = dataclasses.replace(user, password=None)
    await users_repository.commit()
    return updated_user

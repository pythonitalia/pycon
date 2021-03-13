import dataclasses
from datetime import datetime

from pydantic import BaseModel, EmailStr, constr

from users.domain.entities import User
from users.domain.repository import AbstractUsersRepository
from users.domain.services.exceptions import EmailAlreadyUsedError


class RegisterInputModel(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


async def register(
    input: RegisterInputModel, *, users_repository: AbstractUsersRepository
) -> User:
    existing_user = await users_repository.get_by_email(input.email)

    if existing_user:
        raise EmailAlreadyUsedError()

    user = User(
        email=input.email, password=input.password, date_joined=datetime.utcnow()
    )
    created_user = await users_repository.create_user(user)
    # Create a copy of the object, one that sqlalchemy
    # doesn't know about, so using `return created_user`
    # after `commit` will not trigger a new select query
    # not sure if it's a bug of sqlalchemy 1.4 beta
    # but TODO investigate better and fix it :)
    # password=None is required by `replace`
    # but doesn't change the user password or anything
    created_user = dataclasses.replace(created_user, password=None)
    await users_repository.commit()
    return created_user

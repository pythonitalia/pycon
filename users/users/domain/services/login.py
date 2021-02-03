from pydantic import BaseModel, EmailStr, constr

from users.domain.entities import User
from users.domain.repository import AbstractUsersRepository

from .exceptions import UserIsNotActiveError, WrongUsernameOrPasswordError


class LoginInputModel(BaseModel):
    email: EmailStr
    password: constr(min_length=1)


async def login(
    input: LoginInputModel, *, users_repository: AbstractUsersRepository
) -> User:
    user = await users_repository.get_by_email(input.email)

    if not user or not user.check_password(input.password):
        raise WrongUsernameOrPasswordError()

    if not user.is_active:
        raise UserIsNotActiveError()

    return user

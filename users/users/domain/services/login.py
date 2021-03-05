from pydantic import BaseModel, EmailStr, constr

from users.auth.entities import Credential
from users.domain.entities import User
from users.domain.repository import AbstractUsersRepository

from .exceptions import (
    UserIsNotActiveError,
    UserIsNotAdminError,
    WrongEmailOrPasswordError,
)


class LoginInputModel(BaseModel):
    email: EmailStr
    password: constr(min_length=1)


async def login(
    input: LoginInputModel,
    *,
    reject_non_admins: bool = False,
    users_repository: AbstractUsersRepository
) -> User:
    user = await users_repository.get_by_email(input.email)

    if not user or not user.check_password(input.password):
        raise WrongEmailOrPasswordError()

    if not user.is_active:
        raise UserIsNotActiveError()

    if reject_non_admins and Credential.STAFF not in user.credentials.scopes:
        raise UserIsNotAdminError()

    return user

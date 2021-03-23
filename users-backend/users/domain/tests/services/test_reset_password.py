from datetime import datetime, timedelta

import jwt
import time_machine
from ward import raises, test

from users.domain.entities import User
from users.domain.services.exceptions import (
    ResetPasswordTokenExpiredError,
    ResetPasswordTokenInvalidError,
    UserDoesNotExistError,
    UserIsNotActiveError,
)
from users.domain.services.reset_password import ResetPasswordInput, reset_password
from users.domain.tests.fake_repository import FakeUsersRepository
from users.settings import SECRET_KEY


@test("cannot reset password of not active user")
async def _():
    user = User(
        id=10, email="test@email.it", date_joined=datetime.utcnow(), is_active=False
    )

    with raises(UserIsNotActiveError):
        await reset_password(
            ResetPasswordInput(
                token=user.create_reset_password_token(), new_password="testnewpassword"
            ),
            repository=FakeUsersRepository([user]),
        )


@test("cannot reset password with invalidated jwt")
async def _():
    user = User(
        id=10,
        email="test@email.it",
        date_joined=datetime.utcnow(),
        password="old_password",
        is_active=True,
        jwt_auth_id=1,
    )

    token = user.create_reset_password_token()
    user.jwt_auth_id = 2

    with raises(ResetPasswordTokenInvalidError):
        await reset_password(
            ResetPasswordInput(token=token, new_password="testnewpassword"),
            repository=FakeUsersRepository([user]),
        )


@test("cannot reset password with jwt not for reset password")
async def _():
    user = User(
        id=10,
        email="test@email.it",
        date_joined=datetime.utcnow(),
        password="old_password",
        is_active=True,
        jwt_auth_id=1,
    )

    with time_machine.travel("2021-10-10 15:00:00Z", tick=False):
        token = jwt.encode(
            {
                "jti": user.get_reset_password_jwt_id(),
                "user_id": 10,
                "exp": datetime.utcnow() + timedelta(minutes=30),
                "iat": datetime.utcnow(),
                "iss": "users",
                "aud": "users/not-reset-password",
            },
            str(SECRET_KEY),
        )

    with raises(ResetPasswordTokenInvalidError):
        await reset_password(
            ResetPasswordInput(token=token, new_password="testnewpassword"),
            repository=FakeUsersRepository([user]),
        )


@test("cannot reset password with jwt without id")
async def _():
    user = User(
        id=10,
        email="test@email.it",
        date_joined=datetime.utcnow(),
        password="old_password",
        is_active=True,
        jwt_auth_id=1,
    )

    with time_machine.travel("2021-10-10 15:00:00Z", tick=False):
        token = jwt.encode(
            {
                "user_id": 10,
                "exp": datetime.utcnow() + timedelta(minutes=30),
                "iat": datetime.utcnow(),
                "iss": "users",
                "aud": "users/not-reset-password",
            },
            str(SECRET_KEY),
        )

    with raises(ResetPasswordTokenInvalidError):
        await reset_password(
            ResetPasswordInput(token=token, new_password="testnewpassword"),
            repository=FakeUsersRepository([user]),
        )


@test("cannot reset password with jwt of not existent user")
async def _():
    user = User(
        id=10,
        email="test@email.it",
        date_joined=datetime.utcnow(),
        password="old_password",
        is_active=True,
        jwt_auth_id=1,
    )

    with time_machine.travel("2021-10-10 15:00:00Z", tick=False):
        token = jwt.encode(
            {
                "jti": "reset-password:20:1",
                "user_id": 20,
                "exp": datetime.utcnow() + timedelta(minutes=30),
                "iat": datetime.utcnow(),
                "iss": "users",
                "aud": "users/reset-password",
            },
            str(SECRET_KEY),
        )

    with raises(UserDoesNotExistError):
        await reset_password(
            ResetPasswordInput(token=token, new_password="testnewpassword"),
            repository=FakeUsersRepository([user]),
        )


@test("cannot reset password with expired jwt")
async def _():
    user = User(
        id=10,
        email="test@email.it",
        date_joined=datetime.utcnow(),
        password="old_password",
        is_active=True,
        jwt_auth_id=1,
    )

    with time_machine.travel("2020-10-10 10:10:10Z", tick=False):
        token = user.create_reset_password_token()

    with time_machine.travel("2020-10-10 15:10:10Z", tick=False), raises(
        ResetPasswordTokenExpiredError
    ):
        await reset_password(
            ResetPasswordInput(token=token, new_password="testnewpassword"),
            repository=FakeUsersRepository([user]),
        )


@test("reset user password")
async def _():
    user = User(
        id=10,
        email="test@email.it",
        date_joined=datetime.utcnow(),
        password="old_password",
        is_active=True,
        jwt_auth_id=1,
    )

    await reset_password(
        ResetPasswordInput(
            token=user.create_reset_password_token(), new_password="testnewpassword"
        ),
        repository=FakeUsersRepository([user]),
    )

    assert user.new_password == "testnewpassword"
    assert user.jwt_auth_id == 2

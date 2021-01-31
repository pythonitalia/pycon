from datetime import datetime

import pydantic
from ward import raises, test

from users.domain.entities import User
from users.domain.services.exceptions import (
    UserIsNotActiveError,
    UsernameOrPasswordInvalidError,
)
from users.domain.services.login import LoginInputModel, login
from users.domain.tests.fake_repository import FakeUsersRepository


@test("cannot login to not existent email")
async def _():
    repository = FakeUsersRepository(users=[])

    with raises(UsernameOrPasswordInvalidError):
        await login(
            LoginInputModel(email="marco@marco.it", password="hello"),
            users_repository=repository,
        )


@test("cannot login with wrong password")
async def _():
    user = User(
        id=1,
        username="marco",
        password="test",
        email="marco@acierno.it",
        fullname="Marco Acierno",
        name="Marco",
        gender="",
        date_birth=None,
        open_to_newsletter=False,
        open_to_recruiting=False,
        country="",
        date_joined=datetime(2020, 1, 1),
        is_staff=False,
        is_superuser=False,
        is_active=True,
    )
    repository = FakeUsersRepository(users=[user])

    with raises(UsernameOrPasswordInvalidError):
        await login(
            LoginInputModel(email="marco@acierno.it", password="tes"),
            users_repository=repository,
        )


@test("cannot login to not active user")
async def _():
    user = User(
        id=1,
        username="marco",
        password="test",
        email="marco@acierno.it",
        fullname="Marco Acierno",
        name="Marco",
        gender="",
        date_birth=None,
        open_to_newsletter=False,
        open_to_recruiting=False,
        country="",
        date_joined=datetime(2020, 1, 1),
        is_staff=False,
        is_superuser=False,
        is_active=False,
    )
    repository = FakeUsersRepository(users=[user])

    with raises(UserIsNotActiveError):
        await login(
            LoginInputModel(email="marco@acierno.it", password="test"),
            users_repository=repository,
        )


@test("can login")
async def _():
    user = User(
        id=1,
        username="marco",
        password="test",
        email="marco@acierno.it",
        fullname="Marco Acierno",
        name="Marco",
        gender="",
        date_birth=None,
        open_to_newsletter=False,
        open_to_recruiting=False,
        country="",
        date_joined=datetime(2020, 1, 1),
        is_staff=False,
        is_superuser=False,
        is_active=True,
    )
    repository = FakeUsersRepository(users=[user])

    logged_user = await login(
        LoginInputModel(email="marco@acierno.it", password="test"),
        users_repository=repository,
    )

    assert logged_user.id == user.id


@test("cannot login with empty email")
async def _():
    with raises(pydantic.ValidationError) as exc:
        LoginInputModel(email="", password="password")

    errors = exc.raised.errors()
    assert len(errors) == 1
    assert {
        "loc": ("email",),
        "msg": "value is not a valid email address",
        "type": "value_error.email",
    } in errors


@test("cannot login with empty password")
async def _():
    with raises(pydantic.ValidationError) as exc:
        LoginInputModel(email="my@email.it", password="")

    errors = exc.raised.errors()
    assert len(errors) == 1
    assert {
        "loc": ("password",),
        "msg": "ensure this value has at least 1 characters",
        "type": "value_error.any_str.min_length",
        "ctx": {"limit_value": 1},
    } in errors

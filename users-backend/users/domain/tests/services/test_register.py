from datetime import datetime

import pydantic
from ward import raises, test

from users.domain.entities import User
from users.domain.services import RegisterInputModel, register
from users.domain.services.exceptions import EmailAlreadyUsedError
from users.domain.tests.fake_repository import FakeUsersRepository


@test("can register")
async def _():
    repository = FakeUsersRepository(users=[])

    user = await register(
        RegisterInputModel(email="marco@marco.it", password="hello_world"),
        users_repository=repository,
    )

    assert repository.committed
    assert user.id is not None
    assert user.email == "marco@marco.it"
    assert user.check_password("hello_world")


@test("cannot register with an already used email")
async def _():
    repository = FakeUsersRepository(
        users=[User(email="marco@marco.it", date_joined=datetime.utcnow())]
    )

    with raises(EmailAlreadyUsedError):
        await register(
            RegisterInputModel(email="marco@marco.it", password="hello_world"),
            users_repository=repository,
        )


@test("password should be at least 8 chars")
async def _():
    with raises(pydantic.ValidationError) as exc:
        RegisterInputModel(email="hello@python.it", password="short")

    errors = exc.raised.errors()
    assert len(errors) == 1
    assert {
        "loc": ("password",),
        "msg": "ensure this value has at least 8 characters",
        "type": "value_error.any_str.min_length",
        "ctx": {"limit_value": 8},
    } in errors


@test("cannot register with empty email")
async def _():
    with raises(pydantic.ValidationError) as exc:
        RegisterInputModel(email="", password="password")

    errors = exc.raised.errors()
    assert len(errors) == 1
    assert {
        "loc": ("email",),
        "msg": "value is not a valid email address",
        "type": "value_error.email",
    } in errors


@test("cannot register with empty password")
async def _():
    with raises(pydantic.ValidationError) as exc:
        RegisterInputModel(email="my@email.it", password="")

    errors = exc.raised.errors()
    assert len(errors) == 1
    assert {
        "loc": ("password",),
        "msg": "ensure this value has at least 8 characters",
        "type": "value_error.any_str.min_length",
        "ctx": {"limit_value": 8},
    } in errors

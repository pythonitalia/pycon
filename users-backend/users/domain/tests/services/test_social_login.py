from datetime import datetime

import time_machine
from pydantic import ValidationError
from users.domain.entities import User
from users.domain.services import SocialAccount, SocialLoginInput, social_login
from users.domain.tests.fake_repository import FakeUsersRepository
from ward import raises, test
from ward.testing import each


@test("can login with non existent account")
async def _():
    repository = FakeUsersRepository(users=[])

    with time_machine.travel("2020-10-10 10:10:00Z", tick=False):
        user = await social_login(
            SocialLoginInput(
                email="test@me.it",
                social_account=SocialAccount(
                    social_id="1",
                    fullname="Test Account",
                    first_name="Test",
                    last_name="Account",
                ),
            ),
            users_repository=repository,
        )

    assert user
    assert user.id is not None
    assert user.date_joined == datetime(2020, 10, 10, 10, 10, 0)
    assert not user.has_usable_password()
    assert user.fullname == "Test Account"
    assert user.name == "Test"
    assert user.email == "test@me.it"


@test("can login to account with same email")
async def _():
    repository = FakeUsersRepository(
        users=[
            User(
                id=10,
                email="test@me.it",
                date_joined=datetime.utcnow(),
                password="my_password",
                fullname="Hello World",
                name="Hello",
            )
        ]
    )

    user = await social_login(
        SocialLoginInput(
            email="test@me.it",
            social_account=SocialAccount(
                social_id="1",
                fullname="Test Account",
                first_name="Test",
                last_name="Account",
            ),
        ),
        users_repository=repository,
    )

    assert user
    assert user.has_usable_password()
    assert user.check_password("my_password")
    assert user.id == 10
    assert user.fullname == "Hello World"
    assert user.name == "Hello"
    assert user.email == "test@me.it"


@test("cannot social login with an invalid email")
async def _(email=each("", "invalid")):
    with raises(ValidationError) as exc:
        SocialLoginInput(email=email, social_account=SocialAccount(social_id="10"))

    errors = exc.raised.errors()
    assert len(errors) == 1
    assert {
        "loc": ("email",),
        "msg": "value is not a valid email address",
        "type": "value_error.email",
    } in errors


@test("cannot social login without social id")
async def _():
    with raises(ValidationError) as exc:
        SocialLoginInput(
            email="test@email.it", social_account=SocialAccount(social_id="")
        )

    errors = exc.raised.errors()
    assert len(errors) == 1
    assert {
        "loc": ("social_id",),
        "msg": "ensure this value has at least 1 characters",
        "type": "value_error.any_str.min_length",
        "ctx": {"limit_value": 1},
    } in errors

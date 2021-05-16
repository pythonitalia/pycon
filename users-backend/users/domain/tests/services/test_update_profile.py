from datetime import date, datetime, timezone

from ward import raises, test

from users.domain.entities import User
from users.domain.services.exceptions import UserDoesNotExistError, UserIsNotActiveError
from users.domain.services.update_profile import UpdateProfileInput, update_profile
from users.domain.tests.fake_repository import FakeUsersRepository


@test("update profile")
async def _():
    user = User(
        id=10,
        email="test@email.it",
        date_joined=datetime.now(timezone.utc),
        password="password",
        is_active=True,
        jwt_auth_id=1,
        name="Old name",
        fullname="Old fullname",
        gender="f",
        open_to_recruiting=True,
        open_to_newsletter=True,
        date_birth=date(1900, 1, 1),
        country="US",
    )

    user = await update_profile(
        user.id,
        UpdateProfileInput(
            name="New name",
            full_name="Full name",
            gender="m",
            open_to_recruiting=False,
            open_to_newsletter=False,
            date_birth=date(2020, 10, 1),
            country="IT",
        ),
        users_repository=FakeUsersRepository([user]),
    )

    assert user.name == "New name"
    assert user.fullname == "Full name"
    assert user.gender == "m"
    assert user.open_to_recruiting is False
    assert user.open_to_newsletter is False
    assert user.date_birth == date(2020, 10, 1)
    assert user.country == "IT"


@test("cannot update not active user")
async def _():
    user = User(
        id=10,
        email="test@email.it",
        date_joined=datetime.now(timezone.utc),
        password="password",
        is_active=False,
        jwt_auth_id=1,
        name="Old name",
        fullname="Old fullname",
        gender="f",
        open_to_recruiting=True,
        open_to_newsletter=True,
        date_birth=date(1900, 1, 1),
        country="US",
    )

    with raises(UserIsNotActiveError):
        await update_profile(
            user.id,
            UpdateProfileInput(
                name="New name",
                full_name="Full name",
                gender="m",
                open_to_recruiting=False,
                open_to_newsletter=False,
                date_birth=date(2020, 10, 1),
                country="IT",
            ),
            users_repository=FakeUsersRepository([user]),
        )


@test("cannot update if user does not exist")
async def _():
    with raises(UserDoesNotExistError):
        await update_profile(
            5,
            UpdateProfileInput(
                name="New name",
                full_name="Full name",
                gender="m",
                open_to_recruiting=False,
                open_to_newsletter=False,
                date_birth=date(2020, 10, 1),
                country="IT",
            ),
            users_repository=FakeUsersRepository([]),
        )

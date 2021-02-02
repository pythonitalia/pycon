from datetime import datetime
from unittest.mock import MagicMock, patch

from starlette.authentication import AuthenticationError
from ward import raises, test

from users.auth.backend import JWTAuthBackend
from users.auth.entities import Credential
from users.domain.entities import User
from users.domain.tests.fake_repository import FakeUsersRepository


@test("accept valid jwt token")
async def _():
    user = User(
        id=1,
        email="test@user.it",
        name="Name",
        is_staff=False,
        date_joined=datetime.utcnow(),
    )

    repository = FakeUsersRepository(users=[user])

    jwt_token = user.generate_token()

    request = MagicMock()
    request.headers = {"Authorization": f"Bearer {jwt_token}"}

    credentials, logged_user = await JWTAuthBackend(repository).authenticate(request)

    assert credentials.scopes == [Credential.AUTHENTICATED]
    assert logged_user.id == user.id


@test("random token string fails validation")
async def _():
    user = User(
        id=1,
        email="test@user.it",
        name="Name",
        is_staff=False,
        date_joined=datetime.utcnow(),
    )

    repository = FakeUsersRepository(users=[user])

    request = MagicMock()
    request.headers = {"Authorization": f"Bearer abc"}

    with raises(AuthenticationError):
        await JWTAuthBackend(repository).authenticate(request)


@test("invalid token prefix is rejected")
async def _():
    user = User(
        id=1,
        email="test@user.it",
        name="Name",
        is_staff=False,
        date_joined=datetime.utcnow(),
    )

    repository = FakeUsersRepository(users=[user])

    request = MagicMock()
    request.headers = {"Authorization": f"token abc"}

    result = await JWTAuthBackend(repository).authenticate(request)
    assert not result


@test("not active users are rejected")
async def _():
    user = User(
        id=1,
        email="test@user.it",
        name="Name",
        is_staff=False,
        is_active=False,
        date_joined=datetime.utcnow(),
    )

    repository = FakeUsersRepository(users=[user])

    jwt_token = user.generate_token()

    request = MagicMock()
    request.headers = {"Authorization": f"Bearer {jwt_token}"}

    with raises(AuthenticationError):
        await JWTAuthBackend(repository).authenticate(request)


@test("staff users have the correct credentials")
async def _():
    user = User(
        id=1,
        email="test@user.it",
        name="Name",
        is_staff=True,
        is_active=True,
        date_joined=datetime.utcnow(),
    )

    repository = FakeUsersRepository(users=[user])

    jwt_token = user.generate_token()

    request = MagicMock()
    request.headers = {"Authorization": f"Bearer {jwt_token}"}

    credentials, logged_user = await JWTAuthBackend(repository).authenticate(request)

    assert Credential.AUTHENTICATED in credentials.scopes
    assert Credential.STAFF in credentials.scopes
    assert logged_user.id == user.id


@test("not logged request")
async def _():
    repository = FakeUsersRepository(users=[])
    request = MagicMock()
    request.headers = {}

    result = await JWTAuthBackend(repository).authenticate(request)
    assert not result


@test("expired token is rejected")
async def _():
    user = User(
        id=1,
        email="test@user.it",
        name="Name",
        is_staff=False,
        is_active=True,
        date_joined=datetime.utcnow(),
    )

    repository = FakeUsersRepository(users=[user])

    with patch(
        "users.auth.entities.get_jwt_metadata",
        return_value={"exp": datetime(1980, 1, 1), "iat": datetime(1980, 1, 1)},
    ):
        jwt_token = user.generate_token()

    request = MagicMock()
    request.headers = {"Authorization": f"Bearer {jwt_token}"}

    with raises(AuthenticationError):
        await JWTAuthBackend(repository).authenticate(request)

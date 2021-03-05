from datetime import datetime
from unittest.mock import MagicMock

import time_machine
from starlette.authentication import AuthenticationError
from ward import raises, test

from users.auth.backend import PASTAPORTO_X_HEADER, PastaportoAuthBackend
from users.auth.entities import Credential
from users.domain.entities import User
from users.tests.pastaporto import fake_pastaporto_token_for_user


@test("accept valid pastaporto")
async def _():
    user = User(
        id=1,
        email="test@user.it",
        name="Name",
        is_staff=True,
        is_active=True,
        date_joined=datetime.utcnow(),
    )

    fake_pastaporto = fake_pastaporto_token_for_user(user)

    request = MagicMock()
    request.headers = {PASTAPORTO_X_HEADER: fake_pastaporto}

    credentials, logged_user = await PastaportoAuthBackend().authenticate(request)

    assert Credential.AUTHENTICATED in credentials.pastaporto.credentials
    assert Credential.STAFF in credentials.pastaporto.credentials
    assert credentials.pastaporto.user_info.id == user.id
    assert logged_user.id == user.id


@test("rejects expired pastaporto")
async def _():
    user = User(
        id=1,
        email="test@user.it",
        name="Name",
        is_staff=True,
        is_active=True,
        date_joined=datetime.utcnow(),
    )

    with time_machine.travel("2010-10-10 10:10:10", tick=False):
        fake_pastaporto = fake_pastaporto_token_for_user(user)

    request = MagicMock()
    request.headers = {PASTAPORTO_X_HEADER: fake_pastaporto}

    with time_machine.travel("2020-10-10 10:10:10", tick=False), raises(
        AuthenticationError
    ) as exc:
        await PastaportoAuthBackend().authenticate(request)

    assert str(exc.raised) == "Invalid pastaporto"


@test("non-authenticated request does nothing")
async def _():
    request = MagicMock()
    request.headers = {}

    assert await PastaportoAuthBackend().authenticate(request) is None

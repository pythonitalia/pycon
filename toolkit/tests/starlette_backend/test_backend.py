from unittest.mock import MagicMock

import time_machine
from pythonit_toolkit.pastaporto.entities import Credential
from pythonit_toolkit.pastaporto.test import fake_pastaporto_token_for_user
from pythonit_toolkit.starlette_backend.pastaporto_backend import (
    PASTAPORTO_X_HEADER,
    PastaportoAuthBackend,
)
from starlette.authentication import AuthenticationError
from ward import raises, test


@test("accept valid pastaporto")
async def _():
    fake_pastaporto = fake_pastaporto_token_for_user(
        {"id": 1, "email": "test@user.it"}, "testkey", staff=True
    )

    request = MagicMock()
    request.headers = {PASTAPORTO_X_HEADER: fake_pastaporto}

    credentials, logged_user = await PastaportoAuthBackend("testkey").authenticate(
        request
    )

    assert Credential.AUTHENTICATED in credentials.pastaporto.credentials
    assert Credential.STAFF in credentials.pastaporto.credentials
    assert credentials.pastaporto.user_info.id == 1
    assert logged_user.id == 1
    assert logged_user.email == "test@user.it"


@test("rejects expired pastaporto")
async def _():
    with time_machine.travel("2010-10-10 10:10:10", tick=False):
        fake_pastaporto = fake_pastaporto_token_for_user(
            {"id": 1, "email": "testemail@email.it"}, "testkey"
        )

    request = MagicMock()
    request.headers = {PASTAPORTO_X_HEADER: fake_pastaporto}

    with time_machine.travel("2020-10-10 10:10:10", tick=False), raises(
        AuthenticationError
    ) as exc:
        await PastaportoAuthBackend("testkey").authenticate(request)

    assert str(exc.raised) == "Invalid pastaporto"


@test("non-authenticated request does nothing")
async def _():
    request = MagicMock()
    request.headers = {}

    assert await PastaportoAuthBackend("testkey").authenticate(request) is None

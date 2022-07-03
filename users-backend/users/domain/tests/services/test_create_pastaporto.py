from datetime import datetime

from pythonit_toolkit.pastaporto.entities import Credential
from pythonit_toolkit.pastaporto.tokens import decode_pastaporto
from ward import raises, test

from users.domain.entities import User
from users.domain.services.create_pastaporto import (
    create_not_authenticated_pastaporto,
    create_pastaporto,
)
from users.domain.services.exceptions import (
    TokenNotValidAnymoreError,
    UserIsNotActiveError,
)
from users.settings import PASTAPORTO_SECRET


@test("normal user pastaporto")
async def _():
    decoded_identity = {"sub": 1, "jti": "auth:1:1"}

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

    encoded_pastaporto = create_pastaporto(user, decoded_identity)
    decoded_pastaporto = decode_pastaporto(encoded_pastaporto, PASTAPORTO_SECRET)

    assert decoded_pastaporto["user_info"]["id"] == 1
    assert decoded_pastaporto["user_info"]["email"] == "marco@acierno.it"
    assert decoded_pastaporto["user_info"]["is_staff"] is False

    assert decoded_pastaporto["credentials"] == [Credential.AUTHENTICATED]


@test("staff user pastaporto")
async def _():
    decoded_identity = {"sub": 50, "jti": "auth:50:1"}

    user = User(
        id=50,
        username="marco",
        password="test",
        email="test@staff.it",
        fullname="Marco Acierno",
        name="Marco",
        gender="",
        date_birth=None,
        open_to_newsletter=False,
        open_to_recruiting=False,
        country="",
        date_joined=datetime(2020, 1, 1),
        is_staff=True,
        is_superuser=False,
        is_active=True,
    )

    encoded_pastaporto = create_pastaporto(user, decoded_identity)
    decoded_pastaporto = decode_pastaporto(encoded_pastaporto, PASTAPORTO_SECRET)

    assert decoded_pastaporto["user_info"]["id"] == 50
    assert decoded_pastaporto["user_info"]["email"] == "test@staff.it"
    assert decoded_pastaporto["user_info"]["is_staff"] is True

    assert len(decoded_pastaporto["credentials"]) == 2
    assert Credential.AUTHENTICATED in decoded_pastaporto["credentials"]
    assert Credential.STAFF in decoded_pastaporto["credentials"]


@test("cannot create pastaporto of not active user")
async def _():
    decoded_identity = {"sub": 50, "jti": "auth:50:1"}

    user = User(
        id=50,
        username="marco",
        password="test",
        email="test@staff.it",
        fullname="Marco Acierno",
        name="Marco",
        gender="",
        date_birth=None,
        open_to_newsletter=False,
        open_to_recruiting=False,
        country="",
        date_joined=datetime(2020, 1, 1),
        is_staff=True,
        is_superuser=False,
        is_active=False,
    )

    with raises(UserIsNotActiveError):
        create_pastaporto(user, decoded_identity)


@test("cannot create pastaporto if jwt id changed")
async def _():
    decoded_identity = {"sub": 50, "jti": "auth:50:50"}

    user = User(
        id=50,
        jwt_auth_id=40,
        username="marco",
        password="test",
        email="test@staff.it",
        fullname="Marco Acierno",
        name="Marco",
        gender="",
        date_birth=None,
        open_to_newsletter=False,
        open_to_recruiting=False,
        country="",
        date_joined=datetime(2020, 1, 1),
        is_staff=True,
        is_superuser=False,
        is_active=True,
    )

    with raises(TokenNotValidAnymoreError):
        create_pastaporto(user, decoded_identity)


@test("mismatching user and identity are detected and stopped")
async def _():
    decoded_identity = {"sub": 30, "jti": "auth:50:1"}

    user = User(
        id=50,
        jwt_auth_id=1,
        username="marco",
        password="test",
        email="test@staff.it",
        fullname="Marco Acierno",
        name="Marco",
        gender="",
        date_birth=None,
        open_to_newsletter=False,
        open_to_recruiting=False,
        country="",
        date_joined=datetime(2020, 1, 1),
        is_staff=True,
        is_superuser=False,
        is_active=True,
    )

    with raises(ValueError) as exc:
        create_pastaporto(user, decoded_identity)

    assert str(exc.raised) == "Mismatching sub != passed user id"


@test("not authenticated pastaporto")
async def _():
    encoded_pastaporto = create_not_authenticated_pastaporto()
    decoded_pastaporto = decode_pastaporto(encoded_pastaporto, PASTAPORTO_SECRET)

    assert decoded_pastaporto["user_info"] is None
    assert decoded_pastaporto["credentials"] == []

import dataclasses
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from pythonit_toolkit.pastaporto.entities import (
    Credential,
    Pastaporto,
    PastaportoUserInfo,
)

from users.domain.entities import User
from users.domain.services.exceptions import (
    TokenNotValidAnymoreError,
    UserIsNotActiveError,
)
from users.settings import PASTAPORTO_SECRET


def create_pastaporto(user: User, decoded_identity: dict[str, Any]) -> str:
    if not user.is_active:
        raise UserIsNotActiveError()

    if user.get_auth_jwt_id() != decoded_identity["jti"]:
        raise TokenNotValidAnymoreError()

    if decoded_identity["sub"] != user.id:
        raise ValueError("Mismatching sub != passed user id")

    credentials = [Credential.AUTHENTICATED]

    if user.is_staff or user.is_superuser:
        credentials.append(Credential.STAFF)

    return encode_pastaporto(
        Pastaporto(
            user_info=PastaportoUserInfo(
                id=user.id, email=user.email, is_staff=user.is_staff
            ),
            credentials=credentials,
        )
    )


def create_not_authenticated_pastaporto() -> str:
    return encode_pastaporto(Pastaporto(user_info=None, credentials=[]))


def encode_pastaporto(pastaporto: Pastaporto) -> str:
    payload = dataclasses.asdict(pastaporto)
    now = datetime.now(timezone.utc)

    return jwt.encode(
        {
            **payload,
            "exp": now + timedelta(minutes=1),
            "iat": now,
            "iss": "users",
        },
        str(PASTAPORTO_SECRET),
        algorithm="HS256",
    )

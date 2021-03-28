from datetime import datetime, timedelta, timezone

import jwt
from pythonit_toolkit.pastaporto.entities import Credential


def fake_pastaporto_token_for_user(
    user: dict[str, str], secret: str, *, staff: bool = False
):
    credentials = [Credential.AUTHENTICATED]
    if staff:
        credentials.append(Credential.STAFF)

    now = datetime.now(timezone.utc)
    return jwt.encode(
        {
            "userInfo": {"id": user["id"], "email": user["email"]},
            "credentials": credentials,
            "exp": now + timedelta(minutes=1),
            "iat": now,
            "iss": "gateway",
        },
        secret,
        algorithm="HS256",
    )


def fake_service_to_service_token(secret: str, *, issuer: str, audience: str):
    now = datetime.now(timezone.utc)
    return jwt.encode(
        {
            "iss": issuer,
            "aud": audience,
            "exp": now + timedelta(minutes=1),
            "iat": now,
        },
        secret,
        algorithm="HS256",
    )

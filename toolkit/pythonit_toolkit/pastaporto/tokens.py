from datetime import datetime, timedelta, timezone
from typing import Any

import jwt


def decode_pastaporto(token: str, secret: str) -> dict[str, Any]:
    return jwt.decode(
        token,
        str(secret),
        issuer="gateway",
        algorithms=["HS256"],
        options={"require": ["exp", "iss", "iat"]},
    )


def decode_service_to_service_token(
    token: str, secret: str, *, issuer: str, audience: str
):
    return jwt.decode(
        token,
        secret,
        audience=audience,
        issuer=issuer,
        algorithms=["HS256"],
        options={"require": ["exp", "iss", "aud", "iat"]},
    )


def generate_service_to_service_token(secret: str, issuer: str, audience: str):
    if not secret:
        raise ValueError("Secret can not be empty")

    now = datetime.now(tz=timezone.utc)

    return jwt.encode(
        {
            "iss": issuer,
            "aud": audience,
            "iat": now,
            "exp": now + timedelta(seconds=60),
        },
        str(secret),
        algorithm="HS256",
    )

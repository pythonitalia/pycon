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


def generate_service_to_service_token(secret, issuer: str, audience: str):
    if not secret:
        raise ValueError("Secret can not be empty")

    return jwt.encode(
        {
            "issuer": issuer,
            "audience": audience,
            "expires_in": "1m",
        },
        secret,
        algorithm="HS256",
    )

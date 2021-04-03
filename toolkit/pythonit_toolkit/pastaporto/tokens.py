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
        verify=True,
        audience=audience,
        issuer=issuer,
        algorithms=["HS256"],
        options={"require": ["exp", "iss", "aud", "iat"]},
    )

from datetime import datetime, timedelta

import jwt
from pythonit_toolkit.pastaporto.entities import Credential


def fake_pastaporto_token_for_user(
    user: dict[str, str], secret: str, *, staff: bool = False
):
    credentials = [Credential.AUTHENTICATED]
    if staff:
        credentials.append(Credential.STAFF)

    return jwt.encode(
        {
            "userInfo": {"id": user["id"], "email": user["email"]},
            "credentials": credentials,
            "exp": datetime.now() + timedelta(minutes=1),
        },
        secret,
        algorithm="HS256",
    )


def fake_service_to_service_token(secret: str, *, issuer: str, audience: str):
    return jwt.encode(
        {
            "iss": issuer,
            "aud": audience,
            "exp": datetime.now() + timedelta(minutes=1),
        },
        secret,
        algorithm="HS256",
    )

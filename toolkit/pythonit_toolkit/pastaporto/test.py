import datetime

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
            "exp": datetime.now() + datetime.timedelta(minutes=1),
        },
        secret,
        algorithm="HS256",
    )

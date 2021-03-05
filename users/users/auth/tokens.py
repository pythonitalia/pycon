from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any

import jwt

from users.settings import (
    IDENTITY_EXPIRES_AFTER_MINUTES,
    IDENTITY_SECRET,
    PASTAPORTO_SECRET,
)

if TYPE_CHECKING:
    from users.domain.entities import User


def generate_identity_token(user: "User") -> str:
    now = datetime.utcnow()

    payload = {
        "sub": user.id,
        "exp": now + timedelta(minutes=IDENTITY_EXPIRES_AFTER_MINUTES),
        "iat": now,
    }
    return jwt.encode(payload, str(IDENTITY_SECRET), algorithm="HS256")


def decode_pastaporto(token: str) -> dict[str, Any]:
    return jwt.decode(token, str(PASTAPORTO_SECRET), algorithms=["HS256"])

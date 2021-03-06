from datetime import datetime, timedelta
from typing import Any

import jwt


def create_identity_token(
    user_id: int, secret: str, expire_after_minutes: int = 10
) -> str:
    now = datetime.utcnow()

    payload = {
        "sub": user_id,
        "exp": now + timedelta(minutes=expire_after_minutes),
        "iat": now,
    }
    return jwt.encode(payload, str(secret), algorithm="HS256")


def decode_pastaporto(token: str, secret: str) -> dict[str, Any]:
    return jwt.decode(token, str(secret), algorithms=["HS256"])

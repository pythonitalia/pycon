from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any

import jwt


class Action(str, Enum):
    AUTH = "auth"

    def __str__(self) -> str:
        return str.__str__(self)


@dataclass
class PastaportoAction:
    action: Action
    payload: dict[str, Any]

    def sign(self, secret: str) -> str:
        now = datetime.now(timezone.utc)

        return jwt.encode(
            {
                "action": self.action,
                "payload": self.payload,
                "exp": now + timedelta(seconds=40),
                "iat": now,
            },
            str(secret),
            algorithm="HS256",
        )


def create_pastaporto_action(
    action: Action, payload: dict[str, str]
) -> PastaportoAction:
    return PastaportoAction(action=action, payload=payload)


def create_user_auth_pastaporto_action(
    user_id: int, jwt_auth_id: int
) -> PastaportoAction:
    return create_pastaporto_action(
        Action.AUTH, {"id": user_id, "jwtAuthId": jwt_auth_id}
    )

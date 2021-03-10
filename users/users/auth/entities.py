from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from users.settings import JWT_EXPIRES_AFTER_IN_MINUTES

if TYPE_CHECKING:
    from users.domain.entities import Credential, User  # noqa


def get_jwt_metadata() -> dict:
    utcnow = datetime.utcnow()

    return {
        "exp": utcnow + timedelta(minutes=JWT_EXPIRES_AFTER_IN_MINUTES),
        "iat": utcnow,
    }


@dataclass
class JWTToken:
    id: str
    email: str
    name: str
    credentials: list["Credential"]
    exp: datetime
    iat: datetime
    aud: str = "auth"

    @classmethod
    def from_user(cls, user: "User") -> JWTToken:
        return cls(
            id=user.id,
            email=user.email,
            name=user.name,
            credentials=user.credentials.scopes,
            **get_jwt_metadata()
        )

    @classmethod
    def from_payload(cls, payload: dict) -> JWTToken:
        return cls(
            id=payload["id"],
            email=payload["email"],
            name=payload["name"],
            credentials=payload["credentials"],
            exp=payload["exp"],
            iat=payload["iat"],
        )

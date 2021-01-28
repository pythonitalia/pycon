from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import TYPE_CHECKING

from users.settings import JWT_EXPIRES_AFTER_IN_MINUTES

if TYPE_CHECKING:
    from users.domain.entities import User


class Credential(str, Enum):
    AUTHENTICATED = "authenticated"
    STAFF = "staff"

    def __str__(self) -> str:
        return str.__str__(self)


@dataclass
class JWTToken:
    id: str
    email: str
    name: str
    credentials: list[Credential]
    exp: datetime
    iat: datetime
    aud: str = "auth"

    @classmethod
    def from_user(cls, user: "User") -> JWTToken:
        utcnow = datetime.utcnow()
        credentials = [Credential.AUTHENTICATED]

        if user.is_staff:
            credentials.append(Credential.STAFF)

        return cls(
            id=user.id,
            email=user.email,
            name=user.name,
            credentials=credentials,
            exp=utcnow + timedelta(minutes=JWT_EXPIRES_AFTER_IN_MINUTES),
            iat=utcnow,
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

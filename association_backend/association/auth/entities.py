from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

from association.settings import JWT_USERS_JWT_EXPIRES_AFTER_IN_MINUTES


def get_jwt_metadata() -> dict:
    utcnow = datetime.utcnow()

    return {
        "exp": utcnow + timedelta(minutes=JWT_USERS_JWT_EXPIRES_AFTER_IN_MINUTES),
        "iat": utcnow,
    }


class Credential(str, Enum):
    AUTHENTICATED = "authenticated"
    STAFF = "staff"

    def __str__(self) -> str:
        return str.__str__(self)


@dataclass
class User:
    id: str
    email: str
    name: str
    is_staff: False


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
    def from_user(cls, user: User) -> JWTToken:
        credentials = [Credential.AUTHENTICATED]

        if user.is_staff:
            credentials.append(Credential.STAFF)

        return cls(
            id=user.id,
            email=user.email,
            name=user.name,
            credentials=credentials,
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

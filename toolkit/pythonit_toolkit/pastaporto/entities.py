from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

import jwt

from .exceptions import InvalidPastaportoError
from .tokens import decode_pastaporto


class Credential(str, Enum):
    AUTHENTICATED = "authenticated"
    STAFF = "staff"

    def __str__(self) -> str:
        return str.__str__(self)


class RequestAuth:
    scopes: list[Credential]
    pastaporto: Pastaporto

    def __init__(self, pastaporto: Pastaporto):
        self.scopes = pastaporto.credentials
        self.pastaporto = pastaporto


@dataclass
class PastaportoUserInfo:
    id: int
    email: str

    @classmethod
    def from_data(cls, data: dict[str, Any]):
        return cls(id=data["id"], email=data["email"])


@dataclass
class Pastaporto:
    user_info: Optional[PastaportoUserInfo] = None
    credentials: list[Credential] = field(default_factory=list)

    @classmethod
    def from_token(cls, token: str, secret: str):
        try:
            decoded_token = decode_pastaporto(token, secret)
        except (
            ValueError,
            UnicodeDecodeError,
            jwt.ExpiredSignatureError,
            jwt.DecodeError,
            jwt.InvalidAudienceError,
        ):
            raise InvalidPastaportoError()

        user_info = decoded_token.get("userInfo")
        return cls(
            user_info=PastaportoUserInfo.from_data(user_info) if user_info else None,
            credentials=[
                Credential(credential) for credential in decoded_token["credentials"]
            ],
        )

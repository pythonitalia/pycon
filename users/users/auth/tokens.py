import dataclasses
from typing import TYPE_CHECKING

import jwt
from users.auth.entities import JWTToken
from users.settings import JWT_AUTH_SECRET

if TYPE_CHECKING:
    from users.domain.entities import User


def generate_token(user: "User") -> str:
    jwt_token = JWTToken.from_user(user)
    payload = dataclasses.asdict(jwt_token)

    return jwt.encode(payload, str(JWT_AUTH_SECRET), algorithm="HS256")


def decode_token(token: str) -> JWTToken:
    parsed_payload = jwt.decode(
        token, str(JWT_AUTH_SECRET), audience="auth", algorithms=["HS256"]
    )
    return JWTToken.from_payload(parsed_payload)

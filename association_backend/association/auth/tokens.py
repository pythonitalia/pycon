import dataclasses
from typing import Dict

import jwt
from association.auth.entities import JWTToken, User
from association.settings import JWT_USERS_PRIVATE_KEY, JWT_USERS_VERIFY_SIGNATURE


def generate_token(user: User) -> str:
    jwt_token = JWTToken.from_user(user)
    payload = dataclasses.asdict(jwt_token)

    return jwt.encode(payload, str(JWT_USERS_PRIVATE_KEY), algorithm="HS256")


def decode_token(token: str) -> Dict:
    parsed_payload = jwt.decode(
        token,
        key=JWT_USERS_PRIVATE_KEY,
        audience="auth",
        algorithms=["HS256"],
        verify_signature=JWT_USERS_VERIFY_SIGNATURE,
    )
    return JWTToken.from_payload(parsed_payload)

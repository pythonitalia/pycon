from typing import Any

import jwt
from pythonit_toolkit.headers import SERVICE_JWT_HEADER
from pythonit_toolkit.pastaporto.entities import Credential
from pythonit_toolkit.pastaporto.tokens import decode_service_to_service_token
from strawberry.permission import BasePermission
from strawberry.types import Info


class IsAuthenticated(BasePermission):
    message = "Not authenticated"

    def has_permission(self, source, info, **kwargs):
        return Credential.AUTHENTICATED in info.context.request.auth.scopes


def IsService(allowed_callers: list[str], secret: str, service: str):
    if not allowed_callers:
        raise ValueError("No callers allowed specified")

    if not secret:
        raise ValueError("JWT secret cannot be empty")

    if not service:
        raise ValueError("Current service name cannot be empty")

    secret = str(secret)

    class _IsService(BasePermission):
        message = "Forbidden"

        def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
            token = info.context.request.headers.get(SERVICE_JWT_HEADER)

            for caller in allowed_callers:
                try:
                    decode_service_to_service_token(
                        token, secret, issuer=caller, audience=service
                    )
                    return True
                except (
                    jwt.DecodeError,
                    jwt.InvalidIssuerError,
                    jwt.ExpiredSignatureError,
                    jwt.InvalidAudienceError,
                ):
                    pass

            return False

    return _IsService

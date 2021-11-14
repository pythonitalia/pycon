from typing import Any

import jwt
from pythonit_toolkit.headers import SERVICE_JWT_HEADER
from pythonit_toolkit.pastaporto.tokens import decode_service_to_service_token
from strawberry.permission import BasePermission
from strawberry.types import Info

from users.settings import SERVICE_TO_SERVICE_SECRET


def IsService(allowed_callers: list[str]):
    if not allowed_callers:
        raise ValueError("No callers allowed specified")

    class _IsService(BasePermission):
        message = "Forbidden"

        def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
            token = info.context.request.headers.get(SERVICE_JWT_HEADER)
            secret = str(SERVICE_TO_SERVICE_SECRET)

            for caller in allowed_callers:
                try:
                    decode_service_to_service_token(
                        token, secret, issuer=caller, audience="users-service"
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

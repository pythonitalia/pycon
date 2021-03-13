import jwt
from pythonit_toolkit.pastaporto.tokens import decode_service_to_service_token
from starlette.requests import Request

from users.settings import SERVICE_JWT_HEADER, SERVICE_TO_SERVICE_SECRET


def is_service(request: Request) -> bool:
    token = request.headers.get(SERVICE_JWT_HEADER)
    secret = str(SERVICE_TO_SERVICE_SECRET)

    try:
        decode_service_to_service_token(
            token, secret, issuer="gateway", audience="users-service"
        )
        return True
    except (
        jwt.DecodeError,
        jwt.InvalidIssuerError,
        jwt.ExpiredSignatureError,
        jwt.InvalidAudienceError,
    ):
        return False

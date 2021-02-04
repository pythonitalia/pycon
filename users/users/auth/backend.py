import jwt
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
)
from starlette.responses import JSONResponse
from starlette.routing import request_response

from users.auth.tokens import decode_token
from users.domain.repository import AbstractUsersRepository


def on_auth_error(request: request_response, exc: Exception):
    return JSONResponse({"errors": [{"message": str(exc)}]}, status_code=401)


class JWTAuthBackend(AuthenticationBackend):
    users_repository: AbstractUsersRepository

    def __init__(self, users_repository: AbstractUsersRepository) -> None:
        super().__init__()
        self.users_repository = users_repository

    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return

        self.users_repository.with_session(request.state.session)

        auth = request.headers["Authorization"]
        try:
            scheme, token = auth.split()
            if scheme.lower() != "bearer":
                return

            jwt_token = decode_token(token)
        except (
            ValueError,
            UnicodeDecodeError,
            jwt.ExpiredSignatureError,
            jwt.DecodeError,
            jwt.InvalidAudienceError,
        ):
            raise AuthenticationError("Invalid auth credentials")

        user = await self.users_repository.get_by_id(jwt_token.id)

        if not user or not user.is_active:
            raise AuthenticationError("Invalid auth credentials")

        return AuthCredentials(jwt_token.credentials), user

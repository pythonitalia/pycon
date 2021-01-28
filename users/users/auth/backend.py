import jwt
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
)
from users.auth.tokens import decode_token
from users.domain.repository import UsersRepository


class JWTAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return

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

        repository = UsersRepository(request.state.session)
        user = await repository.get_by_id(jwt_token.id)

        if not user or not user.is_active:
            raise AuthenticationError("Invalid auth credentials")

        return AuthCredentials(jwt_token.credentials), user

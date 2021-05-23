from pythonit_toolkit.headers import PASTAPORTO_X_HEADER
from pythonit_toolkit.pastaporto.entities import Pastaporto, RequestAuth
from pythonit_toolkit.pastaporto.exceptions import InvalidPastaportoError
from sentry_sdk import set_user
from starlette.authentication import AuthenticationBackend, AuthenticationError
from starlette.responses import JSONResponse
from starlette.routing import request_response


def on_auth_error(request: request_response, exc: Exception):
    return JSONResponse({"errors": [{"message": str(exc)}]}, status_code=401)


class PastaportoAuthBackend(AuthenticationBackend):
    def __init__(self, secret: str) -> None:
        super().__init__()
        self.pastaporto_secret = secret

    async def authenticate(self, request):
        if PASTAPORTO_X_HEADER not in request.headers:
            # TODO: Always fail request without pastaporto?
            set_user(None)
            return

        pastaporto_token = request.headers[PASTAPORTO_X_HEADER]

        try:
            pastaporto = Pastaporto.from_token(pastaporto_token, self.pastaporto_secret)

            if pastaporto.is_authenticated:
                set_user({"id": pastaporto.user_info.id, "ip_address": "{{auto}}"})
            else:
                set_user(None)

            return RequestAuth(pastaporto), pastaporto.user_info
        except InvalidPastaportoError as e:
            set_user(None)
            raise AuthenticationError("Invalid pastaporto") from e

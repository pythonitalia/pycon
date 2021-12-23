import base64
import binascii

from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    SimpleUser,
)

from src.association.settings import PRETIX_WEBHOOK_SECRET


class PretixAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        if request.url.path != "/pretix-webhook":
            raise ValueError("PretixAuthBackend used outside pretix-webhook")

        if "Authorization" not in request.headers:
            return

        auth = request.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != "basic":
                return
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            raise AuthenticationError("Invalid basic auth credentials") from exc

        username, _, password = decoded.partition(":")
        if username != "pretix":
            raise AuthenticationError("Invalid auth")

        if password != str(PRETIX_WEBHOOK_SECRET):
            raise AuthenticationError("Invalid auth")

        return AuthCredentials(["authenticated", "pretix"]), SimpleUser("pretix")

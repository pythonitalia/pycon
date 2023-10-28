import base64
import binascii
from django.conf import settings
from rest_framework.permissions import BasePermission
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class PretixAuthentication(BaseAuthentication):
    def authenticate(self, request):
        if "Authorization" not in request.headers:
            return None

        auth = request.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != "basic":
                return None

            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error):
            raise AuthenticationFailed()

        username, _, password = decoded.partition(":")
        if username != "pretix":
            raise AuthenticationFailed()

        settings_webhook_secret = settings.PRETIX_WEBHOOK_SECRET
        if not settings_webhook_secret or password != settings_webhook_secret:
            raise AuthenticationFailed()

        return ({"pretix": True}, None)


class IsPretixAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, dict) and request.user["pretix"]

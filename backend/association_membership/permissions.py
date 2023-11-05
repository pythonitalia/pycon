from django.conf import settings
from rest_framework.permissions import BasePermission
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import AuthenticationFailed


class PretixAuthentication(BasicAuthentication):
    www_authenticate_realm = "pretix"

    def authenticate_credentials(self, userid, password, request=None):
        """
        Authenticate the userid and password against username and password
        with optional request for context.
        """
        if userid != "pretix":
            raise AuthenticationFailed()

        settings_webhook_secret = settings.PRETIX_WEBHOOK_SECRET

        if not settings_webhook_secret or password != settings_webhook_secret:
            raise AuthenticationFailed()

        return ({"pretix": True}, None)


class IsPretixAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, dict) and request.user["pretix"]

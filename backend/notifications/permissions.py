from django.conf import settings
from rest_framework.permissions import BasePermission
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import AuthenticationFailed


class SNSAuthentication(BasicAuthentication):
    www_authenticate_realm = "sns"

    def authenticate_credentials(self, userid, password, request=None):
        """
        Authenticate the userid and password against username and password
        with optional request for context.
        """
        if userid != "sns":
            raise AuthenticationFailed()

        settings_sns_webhook_secret = settings.SNS_WEBHOOK_SECRET

        if not settings_sns_webhook_secret or password != settings_sns_webhook_secret:
            raise AuthenticationFailed()

        return ({"sns": True}, None)


class IsSNSAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, dict) and request.user["sns"]

from django.conf import settings
from rest_framework.permissions import BasePermission
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class APIKeyAuthentication(BaseAuthentication):
    server_api_key = None
    user_identifier = None

    def authenticate(self, request):
        request_api_key = request.query_params.get("api_key")
        server_api_key = self.get_server_api_key()

        if not server_api_key:
            raise AuthenticationFailed()

        if request_api_key != server_api_key:
            raise AuthenticationFailed()

        return ({self.user_identifier: True}, None)


class SNSAuthentication(APIKeyAuthentication):
    user_identifier = "sns"

    def get_server_api_key(self):
        return settings.SNS_WEBHOOK_SECRET


class IsSNSAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, dict) and request.user["sns"]

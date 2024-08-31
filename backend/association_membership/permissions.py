from django.conf import settings
from notifications.permissions import APIKeyAuthentication
from rest_framework.permissions import BasePermission


class PretixAuthentication(APIKeyAuthentication):
    user_identifier = "pretix"

    def get_server_api_key(self):
        return settings.PRETIX_WEBHOOK_SECRET


class IsPretixAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, dict) and request.user["pretix"]

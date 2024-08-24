from django.conf import settings
from notifications.permissions import APIKeyAuthentication
from rest_framework.permissions import BasePermission


class PretixAuthentication(APIKeyAuthentication):
    server_api_key = settings.PRETIX_WEBHOOK_SECRET
    user_identifier = "pretix"


class IsPretixAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, dict) and request.user["pretix"]

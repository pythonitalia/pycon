from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
from django.conf import settings
from rest_framework.permissions import BasePermission


class PlainAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        if key != settings.PLAIN_INTEGRATION_TOKEN:
            raise exceptions.AuthenticationFailed("Invalid token.")

        return (
            {
                "plain": True,
            },
            None,
        )


class IsPlainAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, dict) and request.user["plain"]

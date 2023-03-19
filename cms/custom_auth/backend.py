import logging

from asgiref.sync import async_to_sync
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from pythonit_toolkit.service_client import ServiceClient, ServiceError

from django.contrib.auth import get_user_model


logger = logging.getLogger(__name__)


LOGIN_QUERY = """mutation($input: LoginInput!) {
    login(input: $input) {
        __typename
        id
        email
        fullname
    }
}
"""


class UsersAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        client = ServiceClient(
            url=f"{settings.USERS_SERVICE_URL}/internal-api",
            service_name="users-backend",
            caller="pycon-backend",
            jwt_secret=str(settings.SERVICE_TO_SERVICE_SECRET),
        )
        client_execute = async_to_sync(client.execute)
        try:
            login_data = client_execute(
                LOGIN_QUERY,
                {"input": {"email": username, "password": password, "staffOnly": True}},
            ).data
        except ServiceError as e:
            logger.exception("Failed to login in django admin", exc_info=e)
            return None

        if login_data["login"] is None:
            # User not found / not active / or anything else
            return None

        user_data = login_data["login"]
        user_model = get_user_model()

        try:
            django_user = user_model.objects.get(email=user_data["email"])
            django_user.first_name = user_data["fullname"]
            django_user.save()
        except user_model.DoesNotExist:
            django_user = user_model.objects.create(
                email=user_data["email"],
                first_name=user_data["fullname"],
                is_active=True,
                is_staff=True,
                is_superuser=False,
            )
        return django_user

    def get_user(self, user_id):
        user_model = get_user_model()

        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None

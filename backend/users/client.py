from typing import Any

from asgiref.sync import async_to_sync
from django.conf import settings
from pythonit_toolkit.service_client import ServiceClient

GET_USERS_BY_IDS = """query GetUsersByIds($ids: [ID!]!) {
    usersByIds(ids: $ids) {
        id
        displayName
        isActive
        isStaff
        gender
    }
}
"""


def get_users_data_by_ids(ids: list[int]) -> dict[str, dict[str, Any]]:
    client = ServiceClient(
        url=f"{settings.USERS_SERVICE}/internal-api",
        service_name="users-backend",
        caller="pycon-backend",
        jwt_secret=settings.SERVICE_TO_SERVICE_SECRET,
    )
    client_execute = async_to_sync(client.execute)
    users_data = client_execute(GET_USERS_BY_IDS, {"ids": ids}).data
    users_by_id = {user["id"]: user for user in users_data["usersByIds"]}

    return users_by_id

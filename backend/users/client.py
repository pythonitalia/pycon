from typing import Any, Optional

from asgiref.sync import async_to_sync
from django.conf import settings
from pythonit_toolkit.service_client import ServiceClient

GET_USERS_BY_IDS = """query GetUsersByIds($ids: [ID!]!) {
    usersByIds(ids: $ids) {
        id
        email
        fullname
        name
        displayName
        country
        isActive
        isStaff
        gender
    }
}
"""

GET_FULL_USERS_DATA_BY_ID = """query GetFullUsersDataById($ids: [ID!]!) {
    usersByIds(ids: $ids) {
        id
        email
        fullname
        name
        displayName
        isActive
        isStaff
        gender
        country
    }
}
"""

SEARCH_USERS = """
    query searchUsers($query: String!){
        searchUsers(query: $query) {
            id
        }
    }
"""

GET_USERS_BY_EMAILS = """
    query usersByEmails($emails: [String!]!) {
        usersByEmails(emails: $emails) {
            id
            email
        }
    }
"""


def get_users_data_by_ids(ids: list[int]) -> dict[str, dict[str, Any]]:
    return async_to_sync(get_users_data_by_ids_async)(ids)


async def get_users_data_by_ids_async(ids: list[int]) -> dict[str, dict[str, Any]]:
    client = ServiceClient(
        url=f"{settings.USERS_SERVICE_URL}/internal-api",
        service_name="users-backend",
        caller="pycon-backend",
        jwt_secret=settings.SERVICE_TO_SERVICE_SECRET,
    )
    response = await client.execute(GET_USERS_BY_IDS, {"ids": ids})
    users_data = response.data
    users_by_id = {user["id"]: user for user in users_data["usersByIds"]}

    return users_by_id


def get_users_full_data(ids: list[int]) -> dict[str, dict[str, Any]]:
    client = ServiceClient(
        url=f"{settings.USERS_SERVICE_URL}/internal-api",
        service_name="users-backend",
        caller="pycon-backend",
        jwt_secret=settings.SERVICE_TO_SERVICE_SECRET,
    )
    client_execute = async_to_sync(client.execute)
    users_data = client_execute(GET_FULL_USERS_DATA_BY_ID, {"ids": ids}).data
    users_by_id = {user["id"]: user for user in users_data["usersByIds"]}
    return users_by_id


def get_user_data_by_query(query: str):
    client = ServiceClient(
        url=f"{settings.USERS_SERVICE_URL}/internal-api",
        service_name="users-backend",
        caller="pycon-backend",
        jwt_secret=settings.SERVICE_TO_SERVICE_SECRET,
    )
    client_execute = async_to_sync(client.execute)
    users_data = client_execute(SEARCH_USERS, {"query": query}).data

    return [user["id"] for user in users_data["searchUsers"]]


def get_user_by_email(email: str) -> Optional[dict[str, str]]:
    client = ServiceClient(
        url=f"{settings.USERS_SERVICE_URL}/internal-api",
        service_name="users-backend",
        caller="pycon-backend",
        jwt_secret=settings.SERVICE_TO_SERVICE_SECRET,
    )
    client_execute = async_to_sync(client.execute)
    users_data = client_execute(GET_USERS_BY_EMAILS, {"emails": [email]}).data

    if not users_data["usersByEmails"]:
        return None

    return users_data["usersByEmails"][0]

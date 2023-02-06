from typing import Any

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
    client = ServiceClient(
        url=f"{settings.USERS_SERVICE_URL}/internal-api",
        service_name="users-backend",
        caller="pycon-backend",
        jwt_secret=settings.SERVICE_TO_SERVICE_SECRET,
    )
    client_execute = async_to_sync(client.execute)
    users_data = client_execute(GET_USERS_BY_IDS, {"ids": ids}).data
    users_by_id = {user["id"]: user for user in users_data["usersByIds"]}

    return users_by_id


def get_users_full_data(ids: list[int]) -> dict[str, dict[str, any]]:
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

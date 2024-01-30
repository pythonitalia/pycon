import logging

import requests
from django.conf import settings

from users.models import User

logger = logging.getLogger(__name__)


class PlainError(Exception):
    pass


def _raise_mutation_error(data, key: str):
    if data[key]["error"]:
        message = data[key]["error"]["message"]
        if data[key]["error"].get("fields"):
            message += (
                f" {data[key]['error']['fields'][0]['field']}: "
                f"{data[key]['error']['fields'][0]['message']}"
            )
        raise PlainError(message)


def _execute(query, variables):
    try:
        response = requests.post(
            settings.PLAIN_API,
            json={"query": query, "variables": variables},
            headers={"Authorization": f"Bearer {settings.PLAIN_API_TOKEN}"},
        )

        response.raise_for_status()

        data = response.json()

        return data["data"]
    except requests.exceptions.HTTPError as e:
        data = e.response.json()
        raise PlainError(data["errors"][0]["message"]) from e


def create_customer(user: User) -> str:
    from grants.tasks import get_name

    document = """
    mutation createCustomer ($input: UpsertCustomerInput!) {
        upsertCustomer (input: $input) {
            customer {
                id
            }

            error {
                message
                type
                code
                fields {
                    field
                    message
                    type
                }
            }
        }
    }
    """

    response = _execute(
        document,
        variables={
            "input": {
                "identifier": {"emailAddress": user.email},
                "onCreate": {
                    "externalId": user.id,
                    "fullName": get_name(user),
                    "email": {
                        "email": user.email,
                        "isVerified": True,
                    },
                },
                "onUpdate": {
                    "externalId": {"value": user.id},
                    "fullName": {"value": get_name(user)},
                    "email": {
                        "email": user.email,
                        "isVerified": True,
                    },
                },
            }
        },
    )

    _raise_mutation_error(response, "upsertCustomer")

    logger.info("Created new customer for %s on Plain", get_name(user))
    return response["upsertCustomer"]["customer"]["id"]


def _create_thread(customer_id: str, title: str, message: str):
    document = """
    mutation createThread($input: CreateThreadInput!) {
        createThread(input: $input) {
            thread {
                __typename
                id
                externalId
                customer {
                    id
                }
                status
                statusChangedAt {
                    __typename
                    iso8601
                    unixTimestamp
                }
                title
                previewText
                priority
            }
            error {
                __typename
                message
                type
                code
                fields {
                    field
                    message
                    type
                }
            }
        }
    }
    """

    response = _execute(
        document,
        variables={
            "input": {
                "title": title,
                "customerIdentifier": {"customerId": customer_id},
                "components": [{"componentText": {"text": message}}],
            }
        },
    )

    _raise_mutation_error(response, "createThread")
    thread_id = response["createThread"]["thread"]["id"]

    logger.info("Thread created with id: %s", thread_id)
    return thread_id


def send_message(user: User, title: str, message: str) -> str:
    customer_id = create_customer(user)
    return _create_thread(customer_id, title, message)

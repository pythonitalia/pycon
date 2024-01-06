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


def change_customer_status(customer_id: str):
    document = """
    mutation changeCustomerStatus ($input: ChangeCustomerStatusInput!) {
        changeCustomerStatus (input:$input) {
            customer {
                id
            }

            error {
                message
            }
        }
    }
    """

    response = _execute(
        document,
        variables={"input": {"status": "ACTIVE", "customerId": customer_id}},
    )

    if response["changeCustomerStatus"]["error"]:
        if (
            response["changeCustomerStatus"]["error"]["message"]
            == "Customer already is status: ACTIVE"
        ):
            return
        raise PlainError(response["changeCustomerStatus"]["error"]["message"])

    logger.info(
        "Customer set to ACTIVE on Plain",
    )


def _send_chat(customer_id: str, title: str, message: str):
    document = """
    mutation upsertCustomTimelineEntry($input: UpsertCustomTimelineEntryInput!) {
        upsertCustomTimelineEntry(input: $input) {
            result
            timelineEntry {
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
                "customerId": customer_id,
                "title": title,
                "components": [{"componentText": {"text": message}}],
            }
        },
    )

    _raise_mutation_error(response, "upsertCustomTimelineEntry")

    logger.info("Custom timeline entry added on Plain with title '%s'", title)


def send_message(user: User, title: str, message: str):
    customer_id = create_customer(user)
    change_customer_status(customer_id)
    _send_chat(customer_id, title, message)

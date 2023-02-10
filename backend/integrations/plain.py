from typing import TypedDict

import requests
from django.conf import settings


class UserData(TypedDict):
    id: str
    fullname: str
    name: str
    username: str
    email: str


class PlainError(Exception):
    pass


def get_name(user_data: UserData, fallback: str = "<no name specified>"):
    return (
        user_data["fullname"] or user_data["name"] or user_data["username"] or fallback
    )


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


def create_customer(user_data: UserData) -> str:
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
                "identifier": {"externalId": user_data["id"]},
                "onCreate": {
                    "externalId": user_data["id"],
                    "fullName": get_name(user_data),
                    "email": {
                        "email": user_data["email"],
                        "isVerified": True,
                    },
                },
                "onUpdate": {
                    "externalId": {"value": user_data["id"]},
                    "fullName": {"value": get_name(user_data)},
                    "email": {
                        "email": user_data["email"],
                        "isVerified": True,
                    },
                },
            }
        },
    )

    _raise_mutation_error(response, "upsertCustomer")

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


def send_message(user_data: UserData, title: str, message: str):
    customer_id = create_customer(user_data)
    change_customer_status(customer_id)
    _send_chat(customer_id, title, message)

import pytest

from integrations.plain import (
    PlainError,
    _create_thread,
    change_customer_status,
    create_customer,
    send_message,
)
from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_create_user_successful(settings, requests_mock):
    settings.PLAIN_API = "https://api.plain.com/graphql/"
    requests_mock.post(
        settings.PLAIN_API,
        json={
            "data": {
                "upsertCustomer": {
                    "result": "UPDATED",
                    "customer": {"id": "c_ABC25904A1DA4E0A82934234F2"},
                    "error": None,
                }
            }
        },
    )

    user = UserFactory(
        name="Ester",
        full_name="Ester",
        email="ester@example.com",
        username="",
    )

    customer_id = create_customer(user)

    assert customer_id == "c_ABC25904A1DA4E0A82934234F2"


def test_create_user_failed(settings, requests_mock):
    settings.PLAIN_API = "https://api.plain.com/graphql/"
    requests_mock.post(
        settings.PLAIN_API,
        json={
            "data": {
                "upsertCustomer": {
                    "customer": None,
                    "error": {
                        "message": "something went wrong",
                    },
                }
            }
        },
    )

    user = UserFactory(
        name="Ester",
        full_name="Ester",
        email="ester@example.com",
        username="",
    )

    with pytest.raises(PlainError, match="something went wrong"):
        create_customer(user)


def test_change_customer_status_successful(settings, requests_mock):
    settings.PLAIN_API = "https://api.plain.com/graphql/"
    requests_mock.post(
        settings.PLAIN_API,
        json={
            "data": {
                "changeCustomerStatus": {
                    "customer": {"id": "c_01GRV5X4BKVSW0YNAXW954VBY6"},
                    "error": None,
                }
            }
        },
    )

    change_customer_status("c_ABC25904A1DA4E0A82934234F2")


def test_change_customer_status_failed(settings, requests_mock):
    settings.PLAIN_API = "https://api.plain.com/graphql/"
    requests_mock.post(
        settings.PLAIN_API,
        json={
            "data": {
                "changeCustomerStatus": {
                    "customer": None,
                    "error": {"message": "something went wrong"},
                }
            }
        },
    )

    with pytest.raises(PlainError, match="something went wrong"):
        change_customer_status("c_ABC25904A1DA4E0A82934234F2")


def test_change_customer_status_is_already_active(settings, requests_mock):
    settings.PLAIN_API = "https://api.plain.com/graphql/"
    requests_mock.post(
        settings.PLAIN_API,
        json={
            "data": {
                "changeCustomerStatus": {
                    "customer": None,
                    "error": {"message": "Customer already is status: ACTIVE"},
                }
            }
        },
    )

    change_customer_status("c_ABC25904A1DA4E0A82934234F2")


def test_send_chat_successful(settings, requests_mock):
    settings.PLAIN_API = "https://api.plain.com/graphql/"
    requests_mock.post(
        settings.PLAIN_API,
        json={
            "data": {
                "upsertCustomTimelineEntry": {
                    "result": "CREATED",
                    "timelineEntry": {"id": "t_01GRXN6HTBRSERGSGHS60PVGBY"},
                    "error": None,
                }
            }
        },
    )

    _create_thread("c_ABC25904A1DA4E0A82934234F2", title="wtf", message="hello world")


def test_create_thread_failed(settings, requests_mock):
    settings.PLAIN_API = "https://api.plain.com/graphql/"
    requests_mock.post(
        settings.PLAIN_API,
        json={
            "data": {
                "upsertCustomTimelineEntry": {
                    "result": "NOOP",
                    "timelineEntry": None,
                    "error": {
                        "message": "There was a validation error.",
                        "type": "VALIDATION",
                        "code": "input_validation",
                        "fields": [
                            {
                                "field": "customerId",
                                "message": "ID does not match expected format",
                                "type": "VALIDATION",
                            }
                        ],
                    },
                }
            }
        },
    )

    with pytest.raises(
        PlainError,
        match=(
            "There was a validation error. "
            "customerId: ID does not match expected format"
        ),
    ):
        _create_thread(
            "c_ABC25904A1DA4E0A82934234F2", title="wtf", message="hello world"
        )


def test_send_message(settings, requests_mock):
    settings.PLAIN_API = "https://api.plain.com/graphql/"
    requests_mock.post(
        settings.PLAIN_API,
        [
            {
                "json": {
                    "data": {
                        "upsertCustomer": {
                            "result": "UPDATED",
                            "customer": {"id": "c_ABC25904A1DA4E0A82934234F2"},
                            "error": None,
                        }
                    }
                }
            },
            {
                "json": {
                    "data": {
                        "changeCustomerStatus": {
                            "customer": {"id": "c_01GRV5X4BKVSW0YNAXW954VBY6"},
                            "error": None,
                        }
                    }
                }
            },
            {
                "json": {
                    "data": {
                        "upsertCustomTimelineEntry": {
                            "result": "CREATED",
                            "timelineEntry": {"id": "t_01GRXN6HTBRSERGSGHS60PVGBY"},
                            "error": None,
                        }
                    }
                }
            },
        ],
    )

    user = UserFactory(
        name="Ester",
        full_name="Ester",
        email="ester@example.com",
        username="",
    )
    send_message(
        user,
        title="User has replied",
        message="Hello World!",
    )

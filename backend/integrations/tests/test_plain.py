import pytest

from integrations.plain import (
    PlainError,
    _create_thread,
    _create_thread_event,
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


def test_create_thread_event_successful(settings, requests_mock):
    settings.PLAIN_API = "https://api.plain.com/graphql/"
    requests_mock.post(
        settings.PLAIN_API,
        json={
            "data": {
                "createThreadEvent": {
                    "threadEvent": {
                        "__typename": "ThreadEvent",
                        "id": "th_event_0123456789ABCDEFGHILMNOPQR",
                    },
                    "error": None,
                }
            }
        },
    )

    thread_event_id = _create_thread_event(
        "th_123", title="wtf", description="hello world"
    )

    assert thread_event_id == "th_event_0123456789ABCDEFGHILMNOPQR"


def test_create_thread_event_failed(settings, requests_mock):
    settings.PLAIN_API = "https://api.plain.com/graphql/"
    requests_mock.post(
        settings.PLAIN_API,
        json={
            "data": {
                "createThreadEvent": {
                    "error": {
                        "message": "There was a validation error.",
                        "type": "VALIDATION",
                        "code": "input_validation",
                        "fields": [
                            {
                                "field": "threadId",
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
            "threadId: ID does not match expected format"
        ),
    ):
        _create_thread_event("th_123", title="wtf", description="hello world")


def test_create_thread_successful(settings, requests_mock):
    settings.PLAIN_API = "https://api.plain.com/graphql/"
    requests_mock.post(
        settings.PLAIN_API,
        json={
            "data": {
                "createThread": {
                    "thread": {
                        "__typename": "Thread",
                        "id": "th_0123456789ABCDEFGHILMNOPQR",
                        "customer": {"id": "c_0123456789ABCDEFGHILMNOPQR"},
                        "status": "TODO",
                        "statusChangedAt": {
                            "__typename": "DateTime",
                            "iso8601": "2024-01-30T12:52:21.884Z",
                            "unixTimestamp": "1706619141884",
                        },
                        "title": "Marcotte has some questions about his grant",
                        "previewText": "Can I have my grant?",
                        "priority": 2,
                    },
                    "error": None,
                }
            }
        },
    )

    thread_id = _create_thread(
        "c_0123456789ABCDEFGHILMNOPQR", title="wtf", message="hello world"
    )

    assert thread_id == "th_0123456789ABCDEFGHILMNOPQR"


def test_create_thread_failed(settings, requests_mock):
    settings.PLAIN_API = "https://api.plain.com/graphql/"
    requests_mock.post(
        settings.PLAIN_API,
        json={
            "data": {
                "createThread": {
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
                        "createThread": {
                            "thread": {
                                "__typename": "Thread",
                                "id": "th_0123456789ABCDEFGHILMNOPQR",
                                "customer": {"id": "c_0123456789ABCDEFGHILMNOPQR"},
                                "status": "TODO",
                                "statusChangedAt": {
                                    "__typename": "DateTime",
                                    "iso8601": "2024-01-30T12:52:21.884Z",
                                    "unixTimestamp": "1706619141884",
                                },
                                "title": "Marcotte has some questions about his grant",
                                "previewText": "Can I have my grant?",
                                "priority": 2,
                            },
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


def test_send_message_with_existing_thread(settings, requests_mock):
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
                        "createThreadEvent": {
                            "threadEvent": {
                                "__typename": "ThreadEvent",
                                "id": "thevent_0123456789ABCDEFGHILMNOPQR",
                            },
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
        existing_thread_id="th_0123456789ABCDEFGHILMNOPQR",
    )

    assert "createThreadEvent" in requests_mock.last_request.json()["query"]

import json
import logging
from unittest.mock import call, patch

from pytest import fixture

from sqs_messages import process_sqs_messages

SQS_MESSAGE_PAYLOAD = {
    "Records": [
        {
            "messageId": "376a615c-fcd1-44db-ad39-059bbca4d835",
            "receiptHandle": "82adf785-8fed-4f13-a94a-7f083052371f",
            "body": json.dumps({"test": "data", "numbers": 123}),
            "messageAttributes": {"MessageType": {"stringValue": "Type"}},
            "eventSource": "aws:sqs",
        }
    ]
}


@fixture
def mock_boto3():
    with patch("sqs_messages.boto3") as mock_boto3:
        yield mock_boto3


def test_process_sqs_messages(mock_boto3, settings):
    settings.SQS_QUEUE_URL = "sqs://fake-url"

    def fake_handler(data):
        assert data["test"] == "data"
        assert data["numbers"] == 123

    fake_handlers = {"Type": fake_handler}

    with patch("sqs_messages.HANDLERS") as handlers:
        handlers.get = fake_handlers.get
        process_sqs_messages(SQS_MESSAGE_PAYLOAD)

    mock_boto3.client().delete_message.assert_called_once_with(
        QueueUrl=settings.SQS_QUEUE_URL,
        ReceiptHandle="82adf785-8fed-4f13-a94a-7f083052371f",
    )


def test_process_sqs_messages_when_handler_does_not_exist(mock_boto3, caplog):
    caplog.set_level(logging.DEBUG)

    fake_handlers = {"Abc": lambda _: None}

    with patch("sqs_messages.HANDLERS") as handlers:
        handlers.get = fake_handlers.get
        process_sqs_messages(SQS_MESSAGE_PAYLOAD)

    assert caplog.messages == [
        "Received SQS message_id=376a615c-fcd1-44db-ad39-059bbca4d835"
        " message_type=Type but no handler accepts it"
    ]


def test_process_sqs_messages_fails_with_exception(mock_boto3, settings, caplog):
    caplog.set_level(logging.DEBUG)

    settings.SQS_QUEUE_URL = "sqs://fake-url"

    def fake_handler(data):
        raise ValueError("Exception message")

    fake_handlers = {"Type": fake_handler}

    with patch("sqs_messages.HANDLERS") as handlers:
        handlers.get = fake_handlers.get
        process_sqs_messages(SQS_MESSAGE_PAYLOAD)

    mock_boto3.client().delete_message.assert_called_once_with(
        QueueUrl=settings.SQS_QUEUE_URL,
        ReceiptHandle="82adf785-8fed-4f13-a94a-7f083052371f",
    )
    assert caplog.messages == [
        "Failed to process message_id=376a615c-fcd1-44db-ad39-059bbca4d835 (Type)"
    ]


def test_process_sqs_messages_with_multiple_messages(mock_boto3, settings):
    settings.SQS_QUEUE_URL = "sqs://fake-url"

    def fake_handler(data):
        assert data["test"] == "data"
        assert data["numbers"] == 123

    def fake_handler2(data):
        assert data["hello"] == "world"

    fake_handlers = {
        "Type": fake_handler,
        "Type2": fake_handler2,
    }

    with patch("sqs_messages.HANDLERS") as handlers:
        handlers.get = fake_handlers.get
        process_sqs_messages(
            {
                "Records": [
                    {
                        "messageId": "376a615c-fcd1-44db-ad39-059bbca4d835",
                        "receiptHandle": "82adf785-8fed-4f13-a94a-7f083052371f",
                        "body": json.dumps({"test": "data", "numbers": 123}),
                        "messageAttributes": {"MessageType": {"stringValue": "Type"}},
                        "eventSource": "aws:sqs",
                    },
                    {
                        "messageId": "11111111-fcd1-44db-ad39-059bbca4d835",
                        "receiptHandle": "11111111-8fed-4f13-a94a-7f083052371f",
                        "body": json.dumps({"hello": "world"}),
                        "messageAttributes": {"MessageType": {"stringValue": "Type2"}},
                        "eventSource": "aws:sqs",
                    },
                ]
            }
        )

    assert mock_boto3.client().delete_message.call_count == 2
    mock_boto3.client().delete_message.assert_has_calls(
        [
            call(
                QueueUrl=settings.SQS_QUEUE_URL,
                ReceiptHandle="82adf785-8fed-4f13-a94a-7f083052371f",
            ),
            call(
                QueueUrl=settings.SQS_QUEUE_URL,
                ReceiptHandle="11111111-8fed-4f13-a94a-7f083052371f",
            ),
        ],
        any_order=True,
    )


def test_process_sqs_messages_ignores_non_sqs_messages(mock_boto3, caplog):
    caplog.set_level(logging.DEBUG)

    fake_handlers = {"Abc": lambda _: None}

    with patch("sqs_messages.HANDLERS") as handlers:
        handlers.get = fake_handlers.get
        process_sqs_messages(
            {
                "Records": [
                    {
                        "messageId": "376a615c-fcd1-44db-ad39-059bbca4d835",
                        "receiptHandle": "82adf785-8fed-4f13-a94a-7f083052371f",
                        "body": json.dumps({"test": "data", "numbers": 123}),
                        "messageAttributes": {"MessageType": {"stringValue": "Type"}},
                        "eventSource": "aws:sns",
                    }
                ]
            }
        )

    assert caplog.messages == [
        "Skipping message_id=376a615c-fcd1-44db-ad39-059bbca4d835"
        " because it is not coming from SQS"
    ]

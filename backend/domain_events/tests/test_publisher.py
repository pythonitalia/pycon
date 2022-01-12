import json
from unittest.mock import patch

from domain_events.publisher import notify_new_submission, publish_message


def test_publish_message(settings):
    settings.SQS_QUEUE_URL = "sqs://fake-queue"

    with patch("domain_events.publisher.boto3") as mock_boto:
        publish_message("MessageType", {"body": "123"}, deduplication_id="idid")

    mock_boto.resource().Queue.assert_called_with(settings.SQS_QUEUE_URL)
    mock_boto.resource().Queue().send_message.assert_called_once_with(
        MessageBody=json.dumps({"body": "123"}),
        MessageAttributes={
            "MessageType": {"StringValue": "MessageType", "DataType": "String"}
        },
        MessageDeduplicationId="idid",
        MessageGroupId="MessageType",
    )


def test_notify_new_submission():
    with patch("domain_events.publisher.publish_message") as mock_publish:
        notify_new_submission(
            1,
            "test_title",
            "test_elevator_pitch",
            "test_submission_type",
            "test_admin_url",
            42,
            "test_topic",
            10,
        )

    mock_publish.assert_called_once_with(
        "NewCFPSubmission",
        {
            "title": "test_title",
            "elevator_pitch": "test_elevator_pitch",
            "submission_type": "test_submission_type",
            "admin_url": "test_admin_url",
            "topic": "test_topic",
            "duration": "42",
            "speaker_id": 10,
        },
        deduplication_id="1",
    )

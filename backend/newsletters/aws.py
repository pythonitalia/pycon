import typing

import boto3
from django.conf import settings


def _get_client():
    return boto3.client("pinpoint", region_name="eu-central-1")


def get_segment_names() -> typing.Iterable[str]:
    client = _get_client()

    response = client.get_segments(
        ApplicationId=settings.PINPOINT_APPLICATION_ID, PageSize="100"
    )

    for segment in response["SegmentsResponse"]["Item"]:
        yield segment["Name"]


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]  # noqa


def create_cfp_segment(segment_name: str, conference: str):
    client = _get_client()

    response = client.create_segment(
        ApplicationId=settings.PINPOINT_APPLICATION_ID,
        WriteSegmentRequest={
            "Name": segment_name,
            "SegmentGroups": {
                "Groups": [
                    {
                        "Dimensions": [
                            {
                                "UserAttributes": {
                                    "has_sent_submission_to": {
                                        "AttributeType": "INCLUSIVE",
                                        "Values": [conference],
                                    }
                                }
                            }
                        ],
                        "SourceSegments": [],
                        "SourceType": "ANY",
                        "Type": "ANY",
                    }
                ],
                "Include": "ALL",
            },
        },
    )

    return response["SegmentResponse"]


def send_users_to_pinpoint(users: typing.Iterable[typing.Any]):
    # batch only supports 100 at the time
    user_chunks = chunks(list(users), 100)

    for user_chunk in user_chunks:
        data = {
            "Item": [
                {
                    "ChannelType": "EMAIL",
                    "Address": user.email,
                    "Id": user.id,
                    "User": {
                        "UserId": user.id,
                        "UserAttributes": {
                            "Name": [user.name],
                            "has_sent_submission_to": user.submission_sent_to,
                            "is_staff": [str(user.is_staff)],
                        },
                    },
                }
                for user in user_chunk
            ]
        }

        client = _get_client()
        client.update_endpoints_batch(
            ApplicationId=settings.PINPOINT_APPLICATION_ID, EndpointBatchRequest=data
        )

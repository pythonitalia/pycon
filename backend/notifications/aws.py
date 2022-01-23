import typing

import boto3
from django.conf import settings

from newsletters.exporter import Endpoint
from users.models import User


def _get_client():
    return boto3.client("pinpoint", region_name="eu-central-1")


def chunks(arr, n):
    for i in range(0, len(arr), n):
        yield arr[i : i + n]  # noqa


def send_endpoints_to_pinpoint(endpoints: typing.Iterable[Endpoint]):
    # batch only supports 100 at the time
    endpoint_chunks = chunks(list(endpoints), 100)

    for endpoints_chunk in endpoint_chunks:
        data = {"Item": [endpoint.to_item() for endpoint in endpoints_chunk]}

        client = _get_client()
        client.update_endpoints_batch(
            ApplicationId=settings.PINPOINT_APPLICATION_ID, EndpointBatchRequest=data
        )


def send_notification(
    template_name: str,
    users: typing.List[User],
    substitutions: typing.Dict[str, typing.List[str]],
):
    client = _get_client()
    client.send_users_messages(
        ApplicationId=settings.PINPOINT_APPLICATION_ID,
        SendUsersMessageRequest={
            "MessageConfiguration": {
                "EmailMessage": {
                    "FromAddress": "noreply@pycon.it",
                    "Substitutions": substitutions,
                }
            },
            "TemplateConfiguration": {"EmailTemplate": {"Name": template_name}},
            "Users": {str(user.id): {} for user in users},
        },
    )

    # TODO: validate that it has been sent correctly

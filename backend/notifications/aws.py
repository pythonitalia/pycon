import typing
from dataclasses import dataclass

import boto3
from django.conf import settings
from users.models import User


@dataclass
class Endpoint:
    id: typing.Union[str, int]
    name: str
    email: str
    full_name: str
    is_staff: bool
    extra_info: typing.Optional[typing.Dict[str, typing.List[str]]] = None

    def as_item(self):
        user_id = f"test_{self.id}"

        return {
            "ChannelType": "EMAIL",
            "Address": self.email,
            "Id": user_id,
            "User": {
                "UserId": user_id,
                "UserAttributes": {
                    "Name": [self.name],
                    "FullName": [self.full_name],
                    "is_staff": [str(self.is_staff)],
                    **(self.extra_info or {}),
                },
            },
        }


def convert_users_to_endpoints(users: typing.Iterable[User]):
    return [
        Endpoint(
            id=user.id,
            name=user.name,
            email=user.email,
            full_name=user.full_name,
            is_staff=user.is_staff,
        )
        for user in users
    ]


def _get_client():
    return boto3.client("pinpoint", region_name="eu-central-1")


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]  # noqa


def send_endpoints_to_pinpoint(endpoints: typing.Iterable[Endpoint]):
    # batch only supports 100 at the time
    endpoint_chunks = chunks(list(endpoints), 100)

    for endpoints_chunk in endpoint_chunks:
        data = {"Item": [endpoint.as_item() for endpoint in endpoints_chunk]}

        client = _get_client()
        client.update_endpoints_batch(
            ApplicationId=settings.PINPOINT_APPLICATION_ID, EndpointBatchRequest=data
        )

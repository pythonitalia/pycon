from enum import Enum

import boto3
import strawberry
from django.conf import settings

from volunteers_notifications.models import VolunteerDevice


@strawberry.enum
class Platform(Enum):
    ANDROID = "android"
    IOS = "ios"

    @property
    def platform_application_arn(self) -> str:
        if self == Platform.ANDROID:
            return settings.VOLUNTEERS_PUSH_NOTIFICATIONS_ANDROID_ARN

        if self == Platform.IOS:
            return settings.VOLUNTEERS_PUSH_NOTIFICATIONS_IOS_ARN


@strawberry.type
class VolunteersNotificationsMutation:
    @strawberry.mutation
    def register_volunteer_device(self, device_token: str, platform: Platform) -> bool:
        if not platform.platform_application_arn:
            raise ValueError("Push notifications are not enabled in this environment")

        if VolunteerDevice.objects.filter(device_token=device_token).exists():
            return True

        client = boto3.client("sns")
        platform_endpoint = client.create_platform_endpoint(
            PlatformApplicationArn=platform.platform_application_arn,
            Token=device_token,
        )

        VolunteerDevice.objects.get_or_create(
            device_token=device_token,
            endpoint_arn=platform_endpoint["EndpointArn"],
            platform=platform.value,
        )
        return True

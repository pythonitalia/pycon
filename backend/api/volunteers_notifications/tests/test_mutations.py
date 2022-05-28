import pytest

from volunteers_notifications.models import VolunteerDevice

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("platform", ["ios", "android"])
def test_register_volunteers_device(graphql_client, mocker, settings, platform):
    settings.VOLUNTEERS_PUSH_NOTIFICATIONS_IOS_ARN = "arn::ios_arn"
    settings.VOLUNTEERS_PUSH_NOTIFICATIONS_ANDROID_ARN = "arn::android_arn"

    boto3_mock = mocker.patch("api.volunteers_notifications.mutations.boto3")
    boto3_mock.client.return_value.create_platform_endpoint.return_value = {
        "EndpointArn": "arn::endpoint_arn",
    }

    response = graphql_client.query(
        """
        mutation($deviceToken: String!, $platform: Platform!) {
            registerVolunteersDevice(deviceToken: $deviceToken, platform: $platform)
        }
        """,
        variables={"platform": platform.upper(), "deviceToken": "test"},
    )

    assert not response.get("errors")
    assert response["data"]["registerVolunteersDevice"] is True

    device = VolunteerDevice.objects.get()
    assert device.device_token == "test"
    assert device.endpoint_arn == "arn::endpoint_arn"
    assert device.platform == platform
    boto3_mock.client.return_value.create_platform_endpoint.assert_called_with(
        PlatformApplicationArn=settings.VOLUNTEERS_PUSH_NOTIFICATIONS_IOS_ARN
        if platform == "ios"
        else settings.VOLUNTEERS_PUSH_NOTIFICATIONS_ANDROID_ARN,
        Token="test",
    )


@pytest.mark.parametrize("platform", ["ios", "android"])
def test_register_again_the_same_device(graphql_client, mocker, settings, platform):
    settings.VOLUNTEERS_PUSH_NOTIFICATIONS_IOS_ARN = "arn::ios_arn"
    settings.VOLUNTEERS_PUSH_NOTIFICATIONS_ANDROID_ARN = "arn::android_arn"

    VolunteerDevice.objects.create(
        device_token="test", endpoint_arn="arn::endpoint_arn", platform=platform
    )

    boto3_mock = mocker.patch("api.volunteers_notifications.mutations.boto3")
    boto3_mock.client.return_value.create_platform_endpoint.return_value = {
        "EndpointArn": "arn::endpoint_arn",
    }

    response = graphql_client.query(
        """
        mutation($deviceToken: String!, $platform: Platform!) {
            registerVolunteersDevice(deviceToken: $deviceToken, platform: $platform)
        }
        """,
        variables={"platform": platform.upper(), "deviceToken": "test"},
    )

    assert not response.get("errors")
    assert response["data"]["registerVolunteersDevice"] is True

    device = VolunteerDevice.objects.get()
    assert device.device_token == "test"
    assert device.endpoint_arn == "arn::endpoint_arn"
    assert device.platform == platform
    boto3_mock.client.return_value.create_platform_endpoint.assert_not_called()


@pytest.mark.parametrize("platform", ["ios", "android"])
def test_cant_register_if_feature_is_disabled(
    graphql_client, mocker, settings, platform
):
    settings.VOLUNTEERS_PUSH_NOTIFICATIONS_IOS_ARN = ""
    settings.VOLUNTEERS_PUSH_NOTIFICATIONS_ANDROID_ARN = ""

    VolunteerDevice.objects.create(
        device_token="test", endpoint_arn="arn::endpoint_arn", platform=platform
    )

    boto3_mock = mocker.patch("api.volunteers_notifications.mutations.boto3")
    boto3_mock.client.return_value.create_platform_endpoint.return_value = {
        "EndpointArn": "arn::endpoint_arn",
    }

    response = graphql_client.query(
        """
        mutation($deviceToken: String!, $platform: Platform!) {
            registerVolunteersDevice(deviceToken: $deviceToken, platform: $platform)
        }
        """,
        variables={"platform": platform.upper(), "deviceToken": "test"},
    )

    assert (
        response["errors"][0]["message"]
        == "Push notifications are not enabled in this environment"
    )

import json
from django.urls import reverse
from django.test import override_settings


@override_settings(SNS_WEBHOOK_SECRET="test")
def test_sns_webhook_without_auth_fails(rest_api_client):
    response = rest_api_client.post(reverse("sns_webhook"))
    assert response.status_code == 403


@override_settings(SNS_WEBHOOK_SECRET="test")
def test_sns_webhook_with_wrong_auth_fails(rest_api_client):
    response = rest_api_client.post(reverse("sns_webhook") + "?api_key=wrong")
    assert response.status_code == 403


@override_settings(SNS_WEBHOOK_SECRET="test")
def test_sns_webhook(rest_api_client, mocker):
    mocker.patch("notifications.views.verify_event_message", return_value=True)
    run_handler_mock = mocker.patch("notifications.views.run_handler")

    response = rest_api_client.post(
        reverse("sns_webhook") + "?api_key=test",
        headers={"x-amz-sns-message-type": "Notification"},
        data={"Message": json.dumps({"eventType": "Test"})},
    )

    run_handler_mock.assert_called_once_with("sns", "test", {"eventType": "Test"})
    assert response.status_code == 200


@override_settings(SNS_WEBHOOK_SECRET="test")
def test_sns_webhook_with_unverified_message_does_nothing(rest_api_client, mocker):
    mocker.patch("notifications.views.verify_event_message", return_value=False)
    run_handler_mock = mocker.patch("notifications.views.run_handler")

    response = rest_api_client.post(
        reverse("sns_webhook") + "?api_key=test",
        headers={"x-amz-sns-message-type": "Notification"},
        data={"Message": json.dumps({"eventType": "Test"})},
    )

    run_handler_mock.assert_not_called()
    assert response.status_code == 400

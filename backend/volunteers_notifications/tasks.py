import json
import boto3
import logging

logger = logging.getLogger(__name__)


def send_volunteers_push_notification(*, notification_id, volunteers_device_id):
    from volunteers_notifications.models import Notification, VolunteerDevice

    notification = Notification.objects.get(id=notification_id)
    device = VolunteerDevice.objects.get(id=volunteers_device_id)

    sns = boto3.client("sns")
    try:
        logger.info(
            "Publishing notification_id=%s to device_id=%s", notification_id, device.id
        )
        sns.publish(
            TargetArn=device.endpoint_arn,
            Message=json.dumps(
                {
                    "default": notification.body,
                    "APNS": json.dumps(
                        {
                            "aps": {
                                "alert": {
                                    "title": notification.title,
                                    "body": notification.body,
                                },
                                "sound": "default",
                            },
                        }
                    ),
                    "GCM": json.dumps(
                        {
                            "title": notification.title,
                            "message": notification.body,
                        },
                    ),
                }
            ),
            MessageStructure="json",
        )
    except (
        sns.exceptions.EndpointDisabledException,
        sns.exceptions.InvalidParameterException,
    ) as e:
        logger.warning(
            "Known error sending push notification_id=%s to device_id=%s",
            notification_id,
            device.id,
            exc_info=e,
        )
    except Exception as e:
        logger.warning(
            "Failed to push notification_id=%s to device_id=%s",
            notification_id,
            device.id,
            exc_info=e,
        )
        raise

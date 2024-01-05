import json
import logging

import boto3

from users.models import User

logger = logging.getLogger(__name__)


def get_name(user: User, fallback: str = "<no name specified>"):
    return user.full_name or user.name or user.username or fallback


def handle_volunteers_push_notification_sent(data):
    from volunteers_notifications.models import Notification, VolunteerDevice

    notification_id = data["notification_id"]
    volunteers_device_id = data["volunteers_device_id"]

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


HANDLERS = {
    "VolunteersPushNotificationSent": handle_volunteers_push_notification_sent,
}

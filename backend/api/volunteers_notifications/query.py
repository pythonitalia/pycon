from datetime import datetime
from typing import List

import strawberry

from volunteers_notifications.models import Notification as NotificationModel


@strawberry.type
class Notification:
    title: str
    body: str
    sent_at: datetime

    @staticmethod
    def from_django(instance: NotificationModel) -> "Notification":
        return Notification(
            title=instance.title,
            body=instance.body,
            sent_at=instance.created,
        )


@strawberry.type
class VolunteersNotificationsQuery:
    def notifications(self) -> List[Notification]:
        return [
            Notification.from_django(notification)
            for notification in NotificationModel.objects.all()
        ]

from datetime import datetime
from typing import List

import strawberry
from strawberry import ID

from volunteers_notifications.models import Notification as NotificationModel


@strawberry.type
class Notification:
    id: ID
    title: str
    body: str
    sent_at: datetime

    @staticmethod
    def from_django(instance: NotificationModel) -> "Notification":
        return Notification(
            id=instance.id,
            title=instance.title,
            body=instance.body,
            sent_at=instance.created,
        )


@strawberry.type
class VolunteersNotificationsQuery:
    @strawberry.field
    def notifications(self) -> List[Notification]:
        return [
            Notification.from_django(notification)
            for notification in NotificationModel.objects.all()
        ]

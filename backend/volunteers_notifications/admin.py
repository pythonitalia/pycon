from django.contrib import admin
from django.db import transaction

from domain_events.publisher import send_volunteers_push_notification
from volunteers_notifications.models import Notification, VolunteerDevice


def _send_notifications(notification: Notification):
    for device in VolunteerDevice.objects.all():
        send_volunteers_push_notification(
            notification_id=notification.id, volunteers_device_id=device.id
        )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "created",
    )
    readonly_fields = ("created",)

    def save_model(self, request, obj, form, change) -> None:
        if change:
            return super().save_model(request, obj, form, change)

        transaction.on_commit(lambda: _send_notifications(obj))
        return super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None) -> bool:
        if obj:
            return False

        return super().has_change_permission(request, obj)


@admin.register(VolunteerDevice)
class VolunteerDeviceAdmin(admin.ModelAdmin):
    list_display = ("device_token", "platform")
    list_filter = ("platform",)

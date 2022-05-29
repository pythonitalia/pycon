from django.contrib import admin

from domain_events.publisher import send_volunteers_push_notification
from volunteers_notifications.models import Notification, VolunteerDevice


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "created",
    )

    def save_model(self, request, obj, form, change) -> None:
        if change:
            return super().save_model(request, obj, form, change)

        ret = super().save_model(request, obj, form, change)

        for device in VolunteerDevice.objects.all():
            send_volunteers_push_notification(
                notification_id=obj.id, volunteers_device_id=device.id
            )
        return ret

    def has_change_permission(self, request, obj=None) -> bool:
        if obj:
            return False

        return super().has_change_permission(request, obj)


@admin.register(VolunteerDevice)
class VolunteerDeviceAdmin(admin.ModelAdmin):
    list_display = ("device_token", "platform")
    list_filter = ("platform",)

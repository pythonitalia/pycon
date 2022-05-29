from django.db import models
from model_utils.models import TimeStampedModel


class Notification(TimeStampedModel):
    title = models.TextField()
    body = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = [
            "-created",
        ]


class VolunteerDevice(TimeStampedModel):
    class Platform(models.TextChoices):
        ANDROID = "android", "Android"
        IOS = "ios", "iOS"

    user_id = models.IntegerField(verbose_name="user", null=True, blank=True)
    device_token = models.TextField(unique=True, blank=False)
    endpoint_arn = models.TextField(unique=True, blank=False)
    platform = models.CharField(max_length=30, choices=Platform.choices)

    class Meta:
        verbose_name = "Volunteer Device"
        verbose_name_plural = "Volunteers Devices"

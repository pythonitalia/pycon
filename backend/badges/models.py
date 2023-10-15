from django.db import models


class AttendeeConferenceRole(models.Model):
    order_position_id = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="user",
        related_name="+",
    )
    roles = models.JSONField(default=list)
    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
    )

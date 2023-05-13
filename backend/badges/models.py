from django.db import models


class AttendeeConferenceRole(models.Model):
    order_position_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    roles = models.JSONField(default=list)
    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
    )

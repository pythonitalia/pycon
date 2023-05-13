from django.db import models


class AttendeeConferenceRole(models.Model):
    order_position_id = models.IntegerField(null=True)
    user_id = models.IntegerField(null=True)
    roles = models.JSONField()
    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
    )

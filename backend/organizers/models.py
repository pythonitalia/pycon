from django.utils.translation import gettext_lazy as _
from django.db import models
from model_utils.models import TimeStampedModel


class Organizer(TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    slack_oauth_bot_token = models.CharField(
        max_length=255,
        blank=True,
        help_text="Slack OAuth bot token",
        default="",
    )

    email_from_address = models.CharField(
        _("email from address"),
        max_length=600,
        blank=True,
        default="",
    )

    def __str__(self):
        return f"{self.name} ({self.slug})"

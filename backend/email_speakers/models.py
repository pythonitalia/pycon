from conferences.querysets import ConferenceQuerySetMixin
from model_utils.models import TimeStampedModel

from django.db import models


class EmailSpeakerQuerySet(ConferenceQuerySetMixin, models.QuerySet):
    pass


class EmailSpeaker(TimeStampedModel):
    class Status(models.TextChoices):
        draft = "draft", "Draft"
        sent = "sent", "Sent"

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.draft,
        verbose_name="status",
    )
    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        verbose_name="conference",
        related_name="email_speakers",
    )
    subject = models.CharField(max_length=988)
    body = models.TextField()

    send_only_to_speakers_without_ticket = models.BooleanField(default=False)

    sent_at = models.DateTimeField(null=True, blank=True)

    objects = EmailSpeakerQuerySet().as_manager()

    @property
    def is_sent(self):
        return self.status == self.Status.sent

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name_plural = "Emails to speakers"


class EmailSpeakerRecipient(TimeStampedModel):
    class Status(models.TextChoices):
        pending = "pending", "Pending"
        sent = "sent", "Sent"
        failed = "failed", "Failed"

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.sent,
        verbose_name="status",
    )

    email_speaker = models.ForeignKey(
        EmailSpeaker,
        on_delete=models.CASCADE,
        related_name="recipients",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="email_speaker_recipients",
    )
    is_test = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_sent(self):
        return self.status == self.Status.sent

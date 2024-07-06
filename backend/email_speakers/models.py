from conferences.querysets import ConferenceQuerySetMixin
from model_utils.models import TimeStampedModel

from django.db import models


class EmailSpeakerQuerySet(ConferenceQuerySetMixin, models.QuerySet):
    def to_send(self):
        return self.filter(status=self.model.Status.in_progress)


class EmailSpeakerRecipientQuerySet(models.QuerySet):
    def to_send(self):
        return self.filter(status=self.model.Status.pending)


class EmailSpeaker(TimeStampedModel):
    class Status(models.TextChoices):
        draft = "draft", "Draft"
        in_progress = "in_progress", "In progress"
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

    @property
    def is_draft(self):
        return self.status == self.Status.draft

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name_plural = "Emails to speakers"


class EmailSpeakerRecipient(TimeStampedModel):
    class Status(models.TextChoices):
        draft = "draft", "Draft"
        pending = "pending", "Pending"
        sent = "sent", "Sent"
        failed = "failed", "Failed"

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.draft,
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

    objects = EmailSpeakerRecipientQuerySet().as_manager()

    @property
    def is_sent(self):
        return self.status == self.Status.sent

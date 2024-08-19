from django.db import transaction
from django.db.models import Q, UniqueConstraint
from django.utils.safestring import mark_safe
from django.db import models
from users.models import User
from notifications.template_utils import render_template_from_string
from notifications.querysets import EmailTemplateQuerySet, SentEmailQuerySet
from model_utils.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string


class EmailTemplate(TimeStampedModel):
    class Identifier(models.TextChoices):
        proposal_accepted = "proposal_accepted", _("Proposal accepted")
        proposal_rejected = "proposal_rejected", _("Proposal rejected")
        proposal_in_waiting_list = (
            "proposal_in_waiting_list",
            _("Proposal in waiting list"),
        )

        proposal_scheduled_time_changed = (
            "proposal_scheduled_time_changed",
            _("Proposal scheduled time changed"),
        )

        custom = "custom", _("Custom")

    EXPECTED_PLACEHOLDERS = {
        Identifier.proposal_accepted: [
            "proposal_title",
            "conference_name",
            "invitation_url",
            "speaker_name",
            "is_reminder",
        ],
    }

    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        related_name="email_templates",
        verbose_name=_("conference"),
    )
    name = models.CharField(_("name"), max_length=200, blank=True, default="")
    identifier = models.CharField(
        _("identifier"),
        max_length=200,
        choices=Identifier.choices,
    )

    reply_to = models.EmailField(_("reply to"), blank=True, null=True)
    subject = models.TextField(_("subject"))
    preview_text = models.TextField(_("preview text"), blank=True)
    body = models.TextField(_("body"))
    cc_addresses = models.JSONField(_("cc addresses"), default=list, blank=True)
    bcc_addresses = models.JSONField(_("bcc addresses"), default=list, blank=True)

    objects = EmailTemplateQuerySet().as_manager()

    def __str__(self):
        if self.identifier == self.Identifier.custom:
            return f"EmailTemplate {self.name} ({self.conference})"

        return f"EmailTemplate {self.identifier} ({self.conference})"

    def send_email(
        self,
        *,
        recipient: User | None = None,
        recipient_email: str | None = None,
        placeholders: dict = None,
    ):
        if not recipient and not recipient_email:
            raise ValueError("Either recipient or recipient_email must be provided")

        from notifications.tasks import send_pending_emails

        recipient_email = recipient_email or recipient.email
        placeholders = placeholders or {}
        processed_subject = render_template_from_string(
            self.subject, placeholders
        ).replace("\n", "<br/>")
        processed_preview_text = render_template_from_string(
            self.preview_text, placeholders
        ).replace("\n", "<br/>")
        processed_body = mark_safe(
            render_template_from_string(
                self.body,
                placeholders,
            ).replace("\n", "<br/>")
        )

        html_body = render_to_string(
            "notifications/email-template.html",
            {
                "subject": processed_subject,
                "preview_text": processed_preview_text,
                "body": processed_body,
            },
        )

        SentEmail.objects.create(
            email_template=self,
            conference=self.conference,
            recipient=recipient,
            recipient_email=recipient_email,
            placeholders=placeholders,
            subject=processed_subject,
            preview_text=processed_preview_text,
            body=html_body,
            reply_to=self.reply_to,
            cc_addresses=self.cc_addresses,
            bcc_addresses=self.bcc_addresses,
        )

        transaction.on_commit(lambda: send_pending_emails.delay())

    @property
    def is_custom(self):
        return self.identifier == self.Identifier.custom

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["identifier", "conference"],
                condition=~Q(identifier="custom"),
                name="unique_non_custom_identifier_conference",
            )
        ]


class SentEmail(TimeStampedModel):
    class Status(models.TextChoices):
        pending = "pending", _("Pending")
        sent = "sent", _("Sent")

    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        related_name="sent_emails",
        verbose_name=_("conference"),
    )

    status = models.CharField(
        _("status"), max_length=200, choices=Status.choices, default=Status.pending
    )

    email_template = models.ForeignKey(
        "notifications.EmailTemplate",
        on_delete=models.CASCADE,
        related_name="sent_emails",
        verbose_name=_("email template"),
    )
    recipient = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="sent_emails",
        verbose_name=_("recipient"),
        null=True,
        blank=True,
    )
    recipient_email = models.EmailField(_("recipient email"))
    sent_at = models.DateTimeField(_("sent at"), null=True, blank=True)
    placeholders = models.JSONField(_("placeholders"), default=dict)

    subject = models.TextField(_("subject"))
    body = models.TextField(_("body"))
    preview_text = models.TextField(_("preview text"), blank=True)

    reply_to = models.EmailField(_("reply to"), blank=True, default="")
    cc_addresses = models.JSONField(_("cc addresses"), default=list, blank=True)
    bcc_addresses = models.JSONField(_("bcc addresses"), default=list, blank=True)

    message_id = models.TextField(_("message id"), blank=True)

    objects = SentEmailQuerySet().as_manager()

    @property
    def is_pending(self):
        return self.status == self.Status.pending

    def __str__(self):
        return f"Sent email to {self.recipient_email} ({self.email_template})"
from django.utils import timezone
from django.db import transaction
from django.db.models import Q, UniqueConstraint
from django.utils.safestring import mark_safe
from django.db import models
from notifications.rendered_email_template import RenderedEmailTemplate
from users.models import User
from notifications.template_utils import render_template_from_string
from notifications.querysets import EmailTemplateQuerySet, SentEmailQuerySet
from model_utils.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from django.conf import settings


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

        voucher_code = "voucher_code", _("Voucher code")

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

    reply_to = models.EmailField(_("reply to"), blank=True)
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

    def get_processed_body(self, placeholders: dict) -> str:
        return mark_safe(
            render_template_from_string(
                self.body,
                placeholders,
            ).replace("\n", "<br/>")
        )

    def get_processed_subject(self, placeholders: dict) -> str:
        return mark_safe(
            render_template_from_string(self.subject, placeholders).replace(
                "\n", "<br/>"
            )
        )

    def get_processed_preview_text(self, placeholders: dict) -> str:
        return mark_safe(
            render_template_from_string(self.preview_text, placeholders).replace(
                "\n", "<br/>"
            )
        )

    def render(
        self,
        *,
        placeholders: dict = None,
        show_placeholders: bool = False,
    ) -> RenderedEmailTemplate:
        return RenderedEmailTemplate(
            email_template=self,
            show_placeholders=show_placeholders,
            placeholders=placeholders,
        )

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
        processed_email_template = self.render(placeholders=placeholders)

        SentEmail.objects.create(
            email_template=self,
            conference=self.conference,
            from_email=settings.DEFAULT_EMAIL_FROM,
            recipient=recipient,
            recipient_email=recipient_email,
            placeholders=placeholders,
            subject=processed_email_template.subject,
            preview_text=processed_email_template.preview_text,
            body=processed_email_template.html_body,
            text_body=processed_email_template.text_body,
            reply_to=self.reply_to,
            cc_addresses=self.cc_addresses,
            bcc_addresses=self.bcc_addresses,
        )

        transaction.on_commit(lambda: send_pending_emails.delay())

    @property
    def is_custom(self):
        return self.identifier == self.Identifier.custom

    def get_placeholders_available(self):
        return self.EXPECTED_PLACEHOLDERS.get(self.identifier, [])

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
        _("status"),
        max_length=200,
        choices=Status.choices,
        default=Status.pending,
        db_index=True,
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
    text_body = models.TextField(_("text body"))
    preview_text = models.TextField(_("preview text"), blank=True)

    from_email = models.EmailField(_("from email"))
    reply_to = models.EmailField(_("reply to"), blank=True, default="")
    cc_addresses = models.JSONField(_("cc addresses"), default=list, blank=True)
    bcc_addresses = models.JSONField(_("bcc addresses"), default=list, blank=True)

    message_id = models.TextField(_("message id"), blank=True, db_index=True)

    objects = SentEmailQuerySet().as_manager()

    @property
    def is_pending(self):
        return self.status == self.Status.pending

    @property
    def is_bounced(self):
        return self.events.filter(event=SentEmailEvent.Event.bounced).exists()

    @property
    def is_delivered(self):
        return self.events.filter(event=SentEmailEvent.Event.delivered).exists()

    @property
    def is_opened(self):
        return self.events.filter(event=SentEmailEvent.Event.opened).exists()

    def mark_as_sent(self, message_id: str):
        self.status = self.Status.sent
        self.sent_at = timezone.now()
        self.message_id = message_id
        self.save(update_fields=["status", "sent_at", "message_id"])

    def record_event(
        self, event: "SentEmailEvent.Event", timestamp: str, payload: dict
    ):
        SentEmailEvent.objects.create(
            sent_email=self,
            event=event,
            timestamp=timestamp,
            payload=payload,
        )

    def __str__(self):
        return f"Sent email to {self.recipient_email} ({self.email_template})"


class SentEmailEvent(TimeStampedModel):
    class Event(models.TextChoices):
        bounced = "bounced", _("Bounced")
        delivered = "delivered", _("Delivered")
        opened = "opened", _("Opened")
        clicked = "clicked", _("Clicked")
        complaint = "complaint", _("Complaint")
        unsubscribed = "unsubscribed", _("Unsubscribed")
        rejected = "rejected", _("Rejected")
        sent = "sent", _("Sent")

    sent_email = models.ForeignKey(
        "notifications.SentEmail",
        on_delete=models.CASCADE,
        related_name="events",
        verbose_name=_("sent email"),
    )

    event = models.CharField(_("event"), max_length=200, choices=Event.choices)
    timestamp = models.DateTimeField(_("timestamp"))
    payload = models.JSONField(_("payload"), default=dict)

    def __str__(self):
        return f"SentEmailEvent {self.event} for {self.sent_email}"

    class Meta:
        indexes = [
            models.Index(fields=["sent_email", "event"]),
        ]

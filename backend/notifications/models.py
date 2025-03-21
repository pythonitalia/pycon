from django.utils import timezone
from django.db import transaction
from django.db.models import Q, UniqueConstraint
from django.db import models
from notifications.rendered_email_template import RenderedEmailTemplate
from users.models import User
from notifications.querysets import EmailTemplateQuerySet, SentEmailQuerySet
from model_utils.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from django.conf import settings

BASE_PLACEHOLDERS = ["conference"]


class EmailTemplateIdentifier(models.TextChoices):
    proposal_accepted = "proposal_accepted", _("Proposal accepted")
    proposal_scheduled = "proposal_scheduled", _("Proposal scheduled")
    proposal_rejected = "proposal_rejected", _("Proposal rejected")
    proposal_in_waiting_list = (
        "proposal_in_waiting_list",
        _("Proposal in waiting list"),
    )
    proposal_scheduled_time_changed = (
        "proposal_scheduled_time_changed",
        _("Proposal scheduled time changed"),
    )
    proposal_received_confirmation = (
        "proposal_received_confirmation",
        _("Proposal received confirmation"),
    )
    speaker_communication = "speaker_communication", _("Speaker communication")

    voucher_code = "voucher_code", _("Voucher code")

    reset_password = "reset_password", _("[System] Reset password")

    grant_application_confirmation = (
        "grant_application_confirmation",
        _("Grant application confirmation"),
    )
    grant_approved = "grant_approved", _("Grant approved")
    grant_rejected = "grant_rejected", _("Grant rejected")
    grant_waiting_list = "grant_waiting_list", _("Grant waiting list")
    grant_waiting_list_update = (
        "grant_waiting_list_update",
        _("Grant waiting list update"),
    )
    grant_voucher_code = "grant_voucher_code", _("Grant voucher code")

    sponsorship_brochure = "sponsorship_brochure", _("Sponsorship brochure")

    visa_invitation_letter_download = (
        "visa_invitation_letter_download",
        _("Visa invitation letter download"),
    )

    custom = "custom", _("Custom")


class EmailTemplate(TimeStampedModel):
    AVAILABLE_PLACEHOLDERS = {
        EmailTemplateIdentifier.proposal_accepted: [
            *BASE_PLACEHOLDERS,
            "conference_name",
            "proposal_title",
            "proposal_type",
            "speaker_name",
        ],
        EmailTemplateIdentifier.proposal_scheduled: [
            *BASE_PLACEHOLDERS,
            "conference_name",
            "proposal_title",
            "invitation_url",
            "speaker_name",
            "is_reminder",
        ],
        EmailTemplateIdentifier.voucher_code: [
            *BASE_PLACEHOLDERS,
            "voucher_code",
            "voucher_type",
            "user_name",
        ],
        EmailTemplateIdentifier.proposal_rejected: [
            *BASE_PLACEHOLDERS,
            "conference_name",
            "speaker_name",
            "proposal_title",
            "proposal_type",
        ],
        EmailTemplateIdentifier.proposal_in_waiting_list: [
            *BASE_PLACEHOLDERS,
            "conference_name",
            "speaker_name",
            "proposal_title",
            "proposal_type",
        ],
        EmailTemplateIdentifier.proposal_scheduled_time_changed: [
            *BASE_PLACEHOLDERS,
            "conference_name",
            "speaker_name",
            "proposal_title",
            "invitation_url",
        ],
        EmailTemplateIdentifier.grant_application_confirmation: [
            *BASE_PLACEHOLDERS,
            "user_name",
        ],
        EmailTemplateIdentifier.proposal_received_confirmation: [
            *BASE_PLACEHOLDERS,
            "user_name",
            "proposal_title",
            "proposal_url",
        ],
        EmailTemplateIdentifier.grant_approved: [
            *BASE_PLACEHOLDERS,
            "reply_url",
            "start_date",
            "end_date",
            "deadline_date_time",
            "deadline_date",
            "visa_page_link",
            "has_approved_travel",
            "has_approved_accommodation",
            "travel_amount",
            "is_reminder",
        ],
        EmailTemplateIdentifier.grant_rejected: [
            *BASE_PLACEHOLDERS,
            "conference_name",
            "user_name",
        ],
        EmailTemplateIdentifier.grant_waiting_list: [
            *BASE_PLACEHOLDERS,
            "conference_name",
            "user_name",
            "reply_url",
            "grants_update_deadline",
        ],
        EmailTemplateIdentifier.grant_waiting_list_update: [
            *BASE_PLACEHOLDERS,
            "conference_name",
            "user_name",
            "reply_url",
            "grants_update_deadline",
        ],
        EmailTemplateIdentifier.reset_password: [
            "user_name",
            "reset_password_link",
        ],
        EmailTemplateIdentifier.speaker_communication: [
            *BASE_PLACEHOLDERS,
            "user_name",
            "conference_name",
            "body",
            "subject",
        ],
        EmailTemplateIdentifier.grant_voucher_code: [
            *BASE_PLACEHOLDERS,
            "conference_name",
            "voucher_code",
            "user_name",
            "has_approved_accommodation",
            "visa_page_link",
        ],
        EmailTemplateIdentifier.sponsorship_brochure: [
            *BASE_PLACEHOLDERS,
            "brochure_url",
            "conference_name",
        ],
        EmailTemplateIdentifier.visa_invitation_letter_download: [
            *BASE_PLACEHOLDERS,
            "invitation_letter_download_url",
            "has_grant",
            "user_name",
        ],
    }

    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        related_name="email_templates",
        verbose_name=_("conference"),
        blank=True,
        null=True,
    )
    is_system_template = models.BooleanField(_("is system template"), default=False)

    name = models.CharField(_("name"), max_length=200, blank=True, default="")
    identifier = models.CharField(
        _("identifier"),
        max_length=200,
        choices=EmailTemplateIdentifier.choices,
    )

    reply_to = models.EmailField(_("reply to"), blank=True)
    subject = models.TextField(_("subject"))
    preview_text = models.TextField(_("preview text"), blank=True)
    body = models.TextField(_("body"))
    cc_addresses = models.JSONField(_("cc addresses"), default=list, blank=True)
    bcc_addresses = models.JSONField(_("bcc addresses"), default=list, blank=True)

    objects = EmailTemplateQuerySet().as_manager()

    def __str__(self):
        if self.identifier == EmailTemplateIdentifier.custom:
            return f"EmailTemplate {self.name} ({self.conference})"

        return f"EmailTemplate {self.identifier} ({self.conference})"

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

        from notifications.tasks import send_pending_email

        recipient_email = recipient_email or recipient.email

        placeholders = placeholders or {}
        processed_email_template = self.render(placeholders=placeholders)

        if self.is_system_template:
            from_email = settings.DEFAULT_FROM_EMAIL
        else:
            from_email = (
                self.conference.organizer.email_from_address
                or settings.DEFAULT_FROM_EMAIL
            )

        sent_email = SentEmail.objects.create(
            email_template=self,
            conference=self.conference,
            from_email=from_email,
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

        transaction.on_commit(lambda: send_pending_email.delay(sent_email.id))

    @property
    def is_custom(self):
        return self.identifier == EmailTemplateIdentifier.custom

    def get_placeholders_available(self):
        return self.AVAILABLE_PLACEHOLDERS.get(self.identifier, BASE_PLACEHOLDERS)

    def save(self, *args, **kwargs):
        if self.is_system_template and self.conference_id:
            raise ValueError("System templates cannot be associated with a conference")

        if not self.is_system_template and not self.conference_id:
            raise ValueError(
                "Templates must be associated with a conference if not system template"
            )

        return super().save(*args, **kwargs)

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
        failed = "failed", _("Failed")

    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        related_name="sent_emails",
        verbose_name=_("conference"),
        null=True,
        blank=True,
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
    def is_complained(self):
        return self.events.filter(event=SentEmailEvent.Event.complained).exists()

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

    def mark_as_failed(self):
        self.status = self.Status.failed
        self.save(update_fields=["status"])

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
        complained = "complained", _("Complained")
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

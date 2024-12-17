from ordered_model.models import OrderedModel
from visa.managers import InvitationLetterRequestQuerySet
from model_utils.models import TimeStampedModel
from django.db import models
from django.db.models import UniqueConstraint, Q
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import storages


class InvitationLetterRequestStatus(models.TextChoices):
    PENDING = "PENDING", _("Pending")
    PROCESSING = "PROCESSING", _("Processing")
    PROCESSED = "PROCESSED", _("Processed")
    SENT = "SENT", _("Sent")
    REJECTED = "REJECTED", _("Rejected")


class InvitationLetterRequestOnBehalfOf(models.TextChoices):
    SELF = "SELF", _("Self")
    OTHER = "OTHER", _("Other")


def invitation_letter_upload_to(instance, filename):
    return f"invitation_letters/{instance.conference.code}/{instance.id}/{filename}"


def private_storage_getter():
    return storages["private"]


class InvitationLetterRequest(TimeStampedModel):
    objects = InvitationLetterRequestQuerySet().as_manager()

    conference = models.ForeignKey("conferences.Conference", on_delete=models.CASCADE)
    requester = models.ForeignKey("users.User", on_delete=models.CASCADE)
    on_behalf_of = models.CharField(
        _("On behalf of"),
        max_length=20,
        choices=InvitationLetterRequestOnBehalfOf.choices,
        default=InvitationLetterRequestOnBehalfOf.SELF,
    )

    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=InvitationLetterRequestStatus.choices,
        default=InvitationLetterRequestStatus.PENDING,
    )

    # Beneficiary information
    full_name = models.CharField(_("full name"), max_length=300)
    email_address = models.EmailField(_("Email"), blank=True, default="")
    nationality = models.CharField(
        _("Nationality"),
        max_length=100,
    )
    address = models.TextField(_("Address"))
    date_of_birth = models.DateField(_("Date of birth"))
    passport_number = models.CharField(_("Passport number"), max_length=20)
    embassy_name = models.CharField(_("Embassy name"), max_length=300)

    invitation_letter = models.FileField(
        _("Invitation letter"),
        upload_to=invitation_letter_upload_to,
        storage=private_storage_getter,
        blank=True,
        null=True,
    )

    def process(self):
        from visa.tasks import process_invitation_letter_request

        process_invitation_letter_request.delay(invitation_letter_request_id=self.id)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["conference", "requester"],
                condition=Q(on_behalf_of=InvitationLetterRequestOnBehalfOf.SELF),
                name="unique_self_request_per_conference",
            )
        ]


class InvitationLetterOrganizerConfig(TimeStampedModel):
    organizer = models.ForeignKey(
        "organizers.Organizer",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("organizer"),
    )


def invitation_letter_attached_document_upload_to(instance, filename):
    return f"invitation_letter_attached_documents/{instance.invitation_letter_organizer_config.organizer.slug}/{filename}"


class InvitationLetterDocument(OrderedModel, TimeStampedModel):
    invitation_letter_organizer_config = models.ForeignKey(
        "InvitationLetterOrganizerConfig",
        on_delete=models.CASCADE,
        related_name="attached_documents",
        verbose_name=_("invitation letter organizer config"),
    )
    document = models.FileField(
        _("document"),
        upload_to=invitation_letter_attached_document_upload_to,
        storage=private_storage_getter,
        null=True,
        blank=True,
    )
    dynamic_document = models.JSONField(_("dynamic document"), null=True, blank=True)
    order_with_respect_to = "invitation_letter_organizer_config"

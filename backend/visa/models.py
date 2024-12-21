from functools import cached_property
from django.db import transaction

from submissions.models import Submission
from users.models import User
from grants.models import Grant
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
    FAILED_TO_GENERATE = "FAILED_TO_GENERATE", _("Failed to generate")


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

    @property
    def on_behalf_of_other(self):
        return self.on_behalf_of == InvitationLetterRequestOnBehalfOf.OTHER

    @property
    def email(self):
        if self.on_behalf_of_other:
            return self.email_address

        return self.requester.email

    def has_accommodation_via_grant(self):
        grant = self.user_grant

        if not grant:
            return False

        return grant.has_approved_accommodation()

    def has_travel_via_grant(self):
        grant = self.user_grant

        if not grant:
            return False

        return grant.has_approved_travel()

    @property
    def grant_approved_type(self):
        grant = self.user_grant

        if not grant:
            return None

        return grant.approved_type

    @cached_property
    def user_grant(self):
        return Grant.objects.for_conference(self.conference).of_user(self.user).first()

    @cached_property
    def role(self):
        user = self.user

        if not user:
            return "Attendee"

        if (
            Submission.objects.for_conference(self.conference)
            .of_user(user)
            .accepted()
            .exists()
        ):
            return "Speaker"

        return "Attendee"

    @property
    def user(self):
        if self.on_behalf_of_other:
            return User.objects.filter(email=self.email_address).first()

        return self.requester

    def schedule(self):
        from visa.tasks import process_invitation_letter_request

        transaction.on_commit(
            lambda: process_invitation_letter_request.delay(
                invitation_letter_request_id=self.id
            )
        )

    def get_config(self):
        return self.conference.invitation_letter_config

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["conference", "requester"],
                condition=Q(on_behalf_of=InvitationLetterRequestOnBehalfOf.SELF),
                name="unique_self_request_per_conference",
            )
        ]


class InvitationLetterConferenceConfig(TimeStampedModel):
    conference = models.OneToOneField(
        "conferences.Conference",
        on_delete=models.CASCADE,
        related_name="invitation_letter_config",
        verbose_name=_("conference"),
    )

    def __str__(self):
        return f"{self.conference.name} - Invitation Letter Config"


def invitation_letter_attached_document_upload_to(instance, filename):
    return f"invitation_letter_attached_documents/{instance.invitation_letter_conference_config.conference.code}/{filename}"


class InvitationLetterDocument(OrderedModel, TimeStampedModel):
    name = models.CharField(_("name"), max_length=300)
    invitation_letter_conference_config = models.ForeignKey(
        "InvitationLetterConferenceConfig",
        on_delete=models.CASCADE,
        related_name="attached_documents",
        verbose_name=_("Invitation letter conference config"),
    )
    document = models.FileField(
        _("document"),
        upload_to=invitation_letter_attached_document_upload_to,
        storage=private_storage_getter,
        null=True,
        blank=True,
    )
    dynamic_document = models.JSONField(_("dynamic document"), null=True, blank=True)
    order_with_respect_to = "invitation_letter_conference_config"

    def __str__(self):
        return f"Document: {self.name}"


class InvitationLetterAsset(TimeStampedModel):
    invitation_letter_conference_config = models.ForeignKey(
        "InvitationLetterConferenceConfig",
        on_delete=models.CASCADE,
        related_name="assets",
        verbose_name=_("Invitation letter conference config"),
    )
    identifier = models.CharField(_("identifier"), max_length=100)
    image = models.ImageField(
        _("image"),
        upload_to="invitation_letters_assets/",
        storage=private_storage_getter,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Asset: {self.identifier}"

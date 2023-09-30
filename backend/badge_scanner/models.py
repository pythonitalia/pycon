from django.db import models
from model_utils.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _


class BadgeScan(TimeStampedModel):
    scanned_by = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name=_("Scanned By"),
        related_name="+",
    )
    badge_url = models.URLField(_("Badge URL"), max_length=2048)
    scanned_user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Scanned User"),
        related_name="+",
    )
    notes = models.TextField(_("Notes"), blank=True)

    attendee_name = models.CharField(_("Attendee Name"), max_length=2048)
    attendee_email = models.EmailField(_("Attendee Email"), max_length=2048)

    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        verbose_name=_("conference"),
        related_name="badge_scans",
    )


class BadgeScanExport(TimeStampedModel):
    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        verbose_name=_("conference"),
        related_name="badge_scan_exports",
    )
    requested_by = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name=_("Requested By"),
        related_name="+",
    )
    file = models.FileField(_("file"), upload_to="badge_scan_exports")

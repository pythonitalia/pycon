from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from conferences.models import Conference


class SpeakerVoucher(TimeStampedModel):
    conference = models.ForeignKey(
        Conference,
        on_delete=models.PROTECT,
        verbose_name=_("conference"),
        related_name="+",
    )
    user_id = models.IntegerField(verbose_name=_("user"))

    voucher_code = models.TextField(
        help_text=_(
            "Voucher code generated for this speaker. "
            "If the speaker has multiple events, only one code will be generated."
        ),
        blank=False,
        null=False,
    )
    pretix_voucher_id = models.IntegerField(
        help_text=_("ID of the voucher in the Pretix database"),
        blank=False,
        null=False,
    )

    voucher_email_sent_at = models.DateTimeField(
        help_text=_("When the email was last sent"), blank=True, null=True
    )

    class Meta:
        verbose_name = _("Speakers Voucher")
        verbose_name_plural = _("Speakers Vouchers")
        unique_together = (
            "conference",
            "user_id",
        )

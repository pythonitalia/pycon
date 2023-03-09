from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from conferences.models import Conference


class SpeakerVoucher(TimeStampedModel):
    class VoucherType(models.TextChoices):
        SPEAKER = "speaker", _("Speaker")
        CO_SPEAKER = "so_speaker", _("Co-Speaker")

    conference = models.ForeignKey(
        Conference,
        on_delete=models.PROTECT,
        verbose_name=_("conference"),
        related_name="+",
    )
    user_id = models.IntegerField(verbose_name=_("user"))
    voucher_type = models.CharField(
        max_length=20,
        choices=VoucherType.choices,
    )

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
        blank=True,
        null=True,
    )

    voucher_email_sent_at = models.DateTimeField(
        help_text=_("When the email was last sent"), blank=True, null=True
    )

    @staticmethod
    def generate_code() -> str:
        charset = list("ABCDEFGHKLMNPQRSTUVWXYZ23456789")
        random_string = get_random_string(length=20, allowed_chars=charset)
        return f"SPEAKER-{random_string}"

    class Meta:
        verbose_name = _("Speakers Voucher")
        verbose_name_plural = _("Speakers Vouchers")
        unique_together = (
            "conference",
            "user_id",
        )

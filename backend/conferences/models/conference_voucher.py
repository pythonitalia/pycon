from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from conferences.querysets import ConferenceVoucherQuerySet
from model_utils.models import TimeStampedModel

from conferences.models import Conference


class ConferenceVoucher(TimeStampedModel):
    class VoucherType(models.TextChoices):
        SPEAKER = "speaker", _("Speaker")
        CO_SPEAKER = "co_speaker", _("Co-Speaker")
        GRANT = "grant", _("Grant")

    conference = models.ForeignKey(
        Conference,
        on_delete=models.PROTECT,
        verbose_name=_("conference"),
        related_name="+",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name=_("user"),
        related_name="+",
    )
    voucher_type = models.CharField(
        max_length=20,
        choices=VoucherType.choices,
    )

    voucher_code = models.TextField(
        help_text=_(
            "Voucher code generated for this user. "
            "A user can only have one code associated to them."
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

    objects = ConferenceVoucherQuerySet().as_manager()

    def get_voucher_configuration(self):
        if self.voucher_type in (
            ConferenceVoucher.VoucherType.SPEAKER,
            ConferenceVoucher.VoucherType.GRANT,
        ):
            price_mode = "set"
            value = "0.00"
        elif self.voucher_type == ConferenceVoucher.VoucherType.CO_SPEAKER:
            price_mode = "percent"
            value = "25.00"

        return price_mode, value

    @staticmethod
    def generate_code() -> str:
        charset = list("ABCDEFGHKLMNPQRSTUVWXYZ23456789")
        random_string = get_random_string(length=30, allowed_chars=charset)
        return random_string

    class Meta:
        verbose_name = _("Voucher")
        verbose_name_plural = _("Vouchers")
        unique_together = (
            "conference",
            "user",
        )

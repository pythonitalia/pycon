import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel


class Payment(TimeStampedModel):
    STATUS = Choices(
        ('waiting', _('waiting')),
        ('rejected', _('rejected')),
        ('refunded', _('refunded')),
        ('completed', _('completed')),
        ('error', _('error')),
    )

    PROVIDERS = Choices(
        ('stripe', _('stripe')),
        ('bank_transfer', _('bank transfer')),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = StatusField(_('status'))
    provider = StatusField(_('payment provider'), choices_name='PROVIDERS')

    description = models.TextField(_('description'), blank=True, default='')

    transaction_id = models.CharField(
        _('transaction id'),
        max_length=255,
        blank=True,
        help_text=_('Id of the transaction, if applicable'),
    )
    currency = models.CharField(_('currency'), max_length=10)
    total = models.DecimalField(
        _('total'),
        max_digits=9,
        decimal_places=2,
        default='0.0',
    )
    tax = models.DecimalField(
        _('tax'),
        max_digits=9,
        decimal_places=2,
        default='0.0',
    )
    billing_first_name = models.CharField(
        _('billing first name'),
        max_length=256,
        blank=True,
    )
    billing_last_name = models.CharField(
        _('billing last name'),
        max_length=256,
        blank=True,
    )
    billing_address_1 = models.CharField(
        _('billing address 1'),
        max_length=256,
        blank=True,
    )
    billing_address_2 = models.CharField(
        _('billing address 2'),
        max_length=256,
        blank=True,
    )
    billing_city = models.CharField(
        _('billing city'),
        max_length=256,
        blank=True,
    )
    billing_country_code = models.CharField(
        _('billing country code'),
        max_length=2,
        blank=True,
    )
    billing_postcode = models.CharField(
        _('billing postcode'),
        max_length=256,
        blank=True,
    )
    billing_country_area = models.CharField(
        _('billing country area'),
        max_length=256,
        blank=True,
    )
    billing_email = models.EmailField(_('billing email'), blank=True)

    def __str__(self):
        created = f'{self.created:%B %d, %Y %H:%m}'
        return f'{self.currency} {self.total} on {created}'

import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel
from polymorphic.models import PolymorphicModel

from .provider_types import PROVIDER_TYPES, BANKTR_TYPE

class Payment(TimeStampedModel, PolymorphicModel):

    STATUS = Choices(
        ('waiting', _('waiting')),
        ('rejected', _('rejected')),
        ('refunded', _('refunded')),
        ('completed', _('completed')),
        ('error', _('error')),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = StatusField(_('status'))
    provider = models.CharField(_('payment provider'), max_length=10, choices=PROVIDER_TYPES)

    description = models.TextField(_('description'), blank=True, default='')

    currency = models.CharField(_('currency'), max_length=10)
    amount = models.DecimalField(
        _('amount'),
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

    def _get_payment_type(self):
        return BANKTR_TYPE

    def capture(self, **kwargs):
        raise NotImplementedError()

    def refund(self):
        self.status = 'refunded'
        self.save()

    def __str__(self):
        created = f'{self.created:%B %d, %Y %H:%m}'
        return f'{self.currency} {self.amount} on {created}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.provider = self._get_payment_type()

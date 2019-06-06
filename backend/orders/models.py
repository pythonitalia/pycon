from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_fsm import FSMField, transition, RETURN_VALUE
from model_utils.models import TimeStampedModel

from payments.providers import PROVIDERS, get_provider


class Order(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_('user'),
        related_name='orders',
    )

    provider = models.CharField(
        max_length=10,
        choices=PROVIDERS,
    )

    transaction_id = models.TextField(
        _('transaction id'),
        blank=True,
        default=''
    )

    state = FSMField(default='new')

    amount = models.DecimalField(
        _('amount'),
        max_digits=10,
        decimal_places=2
    )

    @transition(
        field=state,
        source='new',
        target=RETURN_VALUE(
            'complete',
        ),
        on_error='failed'
    )
    def charge(self, payload):
        """
        Executes the payment using the provider specified
        """
        provider_class = get_provider(self.provider)

        if not provider_class:
            raise ValueError(_('Provider %(provider)s not known!') % {'provider': self.provider})

        provider = provider_class()
        provider.charge(order=self, payload=payload)
        return 'complete'

class OrderItem(TimeStampedModel):
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.PROTECT,
        verbose_name=_('order'),
        related_name='items',
    )

    description = models.CharField(
        _('description'),
        max_length=256
    )

    unit_price = models.DecimalField(
        _('unit price'),
        max_digits=10,
        decimal_places=2
    )

    quantity = models.PositiveIntegerField(_('quantity'))

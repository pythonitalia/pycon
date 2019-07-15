from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_fsm import FSMIntegerField, transition, RETURN_VALUE

from model_utils.models import TimeStampedModel

from payments.providers import PROVIDERS, get_provider

from .enums import PaymentState


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

    state = FSMIntegerField(
        default=PaymentState.NEW,
        choices=PaymentState.choices()
    )

    amount = models.DecimalField(
        _('amount'),
        max_digits=10,
        decimal_places=2
    )

    @transition(field=state, source=PaymentState.NEW, target=PaymentState.PROCESSING, on_error=PaymentState.FAILED)
    def charge(self, payload={}):
        """
        Executes the payment using the provider specified
        """
        provider_class = get_provider(self.provider)

        if not provider_class:
            raise ValueError(_('Provider %(provider)s not known!') % {'provider': self.provider})

        provider = provider_class()
        response = provider.charge(order=self, payload=payload)

        self.order = PaymentState.PROCESSING
        return response

    @transition(field=state, source=PaymentState.PROCESSING, target=RETURN_VALUE(PaymentState.COMPLETE), on_error=PaymentState.FAILED)
    def fullfil(self):
        """
        Call this method to fullfil the order
        """
        for item in self.items.all():
            item.fullfil()

        return PaymentState.COMPLETE

    @transition(field=state, source='*', target=RETURN_VALUE(PaymentState.FAILED), on_error=PaymentState.FAILED)
    def fail(self):
        """
        If something went wrong
        """
        return PaymentState.FAILED


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

    item_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_('item type')
    )
    item_object_id = models.PositiveIntegerField(_('item object id'))
    item_object = GenericForeignKey('item_type', 'item_object_id')

    def fullfil(self):
        for _ in range(0, self.quantity):
            self.item_object.fullfil(
                order=self.order,
                user=self.order.user
            )

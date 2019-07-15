from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel


class Ticket(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_('user'),
        related_name='tickets',
    )

    ticket_fare = models.ForeignKey(
        'conferences.TicketFare',
        on_delete=models.PROTECT,
        verbose_name=_('ticket fare')
    )

    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.PROTECT,
        verbose_name=_('order'),
    )

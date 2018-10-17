from django.db import models

from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeFramedModel, TimeStampedModel


class Ticket(TimeFramedModel, TimeStampedModel):
    conference = models.ForeignKey('conferences.Conference', on_delete=models.CASCADE, verbose_name=_('conference'), related_name='tickets')

    name = models.CharField(_('name'), max_length=100)  # Early Bird Student
    description = models.TextField(_('description'))
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    code = models.CharField(_('code'), max_length=10)

    def __str__(self):
        return f'{self.name} ({self.conference.name})'

    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')
        unique_together = ('conference', 'code',)

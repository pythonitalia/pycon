from django.db import models
from django.core import exceptions
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from model_utils.models import TimeFramedModel


class Deadline(TimeFramedModel):
    TYPES = Choices(
        ('cfp', _('Call for proposal')),
        ('voting', _('Voting')),
        ('refund', _('Ticket refund')),
        ('custom', _('Custom deadline')),
    )

    conference = models.ForeignKey(
        'conferences.Conference',
        on_delete=models.CASCADE,
        verbose_name=_('conference'),
        related_name='deadlines'
    )

    name = models.CharField(_('name'), max_length=100, blank=True, default='')
    type = models.CharField(_('type'), choices=TYPES, max_length=10)

    def clean(self):
        super().clean()

        if self.start > self.end:
            raise exceptions.ValidationError(_('Start date cannot be after end'))

        if self.type != Deadline.TYPES.custom:
            if Deadline.objects.filter(
                    conference=self.conference,
                    type=self.type
            ).exclude(id=self.id).exists():
                raise exceptions.ValidationError(
                    _('You can only have one deadline of type %(type)s') % {'type': self.type}
                )

    def __str__(self):
        return f'{self.type} ({self.name}) <{self.conference.code}>'

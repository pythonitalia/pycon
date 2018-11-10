from django.db import models

from django.core import exceptions
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from model_utils.models import TimeFramedModel, TimeStampedModel


class Conference(TimeStampedModel):
    name = models.CharField(_('name'), max_length=100)
    code = models.CharField(_('code'), max_length=10, unique=True)

    topics = models.ManyToManyField('conferences.Topic', verbose_name=_('topics'))
    languages = models.ManyToManyField('languages.Language', verbose_name=_('languages'))

    def __str__(self):
        return f'{self.name} <{self.code}>'

    class Meta:
        verbose_name = _('Conference')
        verbose_name_plural = _('Conferences')


class Deadline(TimeFramedModel):
    TYPES = Choices(
        ('event', _('Conference')),
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
            if Deadline.objects.filter(conference=self.conference, type=self.type).exclude(id=self.id).exists():
                raise exceptions.ValidationError(
                    _('You can only have one deadline of type %(type)s') % {'type': self.type}
                )

    def __str__(self):
        return f'{self.type} ({self.name}) <{self.conference.code}>'


class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')

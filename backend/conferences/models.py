from django.db import models
from django.utils import timezone
from django.core import exceptions
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from model_utils.models import TimeFramedModel, TimeStampedModel


class Conference(TimeFramedModel, TimeStampedModel):
    name = models.CharField(_('name'), max_length=100)
    code = models.CharField(_('code'), max_length=10, unique=True)

    topics = models.ManyToManyField('conferences.Topic', verbose_name=_('topics'))
    languages = models.ManyToManyField('languages.Language', verbose_name=_('languages'))
    audience_levels = models.ManyToManyField('conferences.AudienceLevel', verbose_name=_('audience levels'))
    submission_types = models.ManyToManyField('submissions.SubmissionType', verbose_name=_('submission types'))

    @property
    def is_cfp_open(self):
        try:
            cfp_deadline = self.deadlines.get(type=Deadline.TYPES.cfp)

            now = timezone.now()
            return cfp_deadline.start <= now <= cfp_deadline.end
        except Deadline.DoesNotExist:
            return False

    def __str__(self):
        return f'{self.name} <{self.code}>'

    class Meta:
        verbose_name = _('Conference')
        verbose_name_plural = _('Conferences')


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


class AudienceLevel(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Audience Level')
        verbose_name_plural = _('Audience Levels')


class Duration(models.Model):
    conference = models.ForeignKey(
        'conferences.Conference',
        on_delete=models.CASCADE,
        verbose_name=_('conference'),
        related_name='durations'
    )

    name = models.CharField(_('name'), max_length=100)
    duration = models.PositiveIntegerField(_('duration'), validators=[MinValueValidator(1)])
    notes = models.TextField(_('notes'), blank=True)

    def __str__(self):
        return f'{self.name} - {self.duration} mins ({self.conference_id})'

    class Meta:
        verbose_name = _('Duration')
        verbose_name_plural = _('Durations')

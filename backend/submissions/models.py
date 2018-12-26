from django.core import exceptions
from django.conf import settings
from django.db import models

from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel


class Submission(TimeStampedModel):
    conference = models.ForeignKey(
        'conferences.Conference',
        on_delete=models.CASCADE,
        verbose_name=_('conference'),
        related_name='submissions'
    )

    title = models.CharField(_('title'), max_length=100)
    abstract = models.TextField(_('abstract'), max_length=1000)
    elevator_pitch = models.TextField(_('elevator pitch'), max_length=300)
    notes = models.TextField(_('notes'))

    speaker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('owner'),
        on_delete=models.SET_NULL,
        null=True,
        related_name='submissions'
    )

    topic = models.ForeignKey('conferences.Topic', verbose_name=_('topic'), on_delete=models.SET_NULL, null=True)
    language = models.ForeignKey('languages.Language', verbose_name=_('language'), on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey('submissions.SubmissionType', verbose_name=_('type'), on_delete=models.SET_NULL, null=True)

    def clean(self):
        if self.topic_id and not self.conference.topics.filter(id=self.topic_id).exists():
            raise exceptions.ValidationError(
                {'topic': _('%(topic)s is not a valid topic') % {'topic': str(self.topic)}}
            )

        if self.language_id and not self.conference.languages.filter(id=self.language_id).exists():
            raise exceptions.ValidationError(
                {'language': _('%(language)s is not an allowed language') % {'language': str(self.language)}}
            )

        if self.type_id and not self.conference.submission_types.filter(id=self.type_id).exists():
            raise exceptions.ValidationError(
                {'type': _('%(submission_type)s is not an allowed submission type') % {'submission_type': str(self.type)}}
            )


class SubmissionType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

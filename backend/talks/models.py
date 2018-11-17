from django.core import exceptions
from django.conf import settings
from django.db import models

from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel


class Talk(TimeStampedModel):
    conference = models.ForeignKey('conferences.Conference', on_delete=models.CASCADE, verbose_name=_('conference'))

    title = models.CharField(_('title'), max_length=100)
    abstract = models.TextField(_('abstract'), max_length=1000)
    elevator_pitch = models.TextField(_('elevator pitch'), max_length=300)
    notes = models.TextField(_('notes'))

    speaker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('owner'),
        on_delete=models.SET_NULL,
        null=True,
        related_name='talks'
    )

    topic = models.ForeignKey('conferences.Topic', verbose_name=_('topic'), on_delete=models.SET_NULL, null=True)
    language = models.ForeignKey('languages.Language', verbose_name=_('language'), on_delete=models.SET_NULL, null=True)

    def clean(self):
        if self.topic_id and not self.conference.topics.filter(id=self.topic_id).exists():
            raise exceptions.ValidationError(
                {'topic': _('%(topic)s is not a valid topic') % {'topic': str(self.topic)}}
            )

        if self.language_id and not self.conference.languages.filter(id=self.language_id).exists():
            raise exceptions.ValidationError(
                {'language': _('%(language)s is not an allowed language') % {'language': str(self.language)}}
            )

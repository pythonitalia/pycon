from django.core import exceptions
from django.conf import settings
from django.db import models

from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel


class Talk(TimeStampedModel):
    conference = models.ForeignKey('conferences.Conference', on_delete=models.CASCADE, verbose_name=_('conference'))

    title = models.CharField(_('title'), max_length=100)
    abstract = models.TextField(_('abstract'), max_length=1000)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('owner'),
        on_delete=models.SET_NULL,
        null=True,
        related_name='talks'
    )

    topic = models.ForeignKey('conferences.Topic', verbose_name=_('topic'), on_delete=models.SET_NULL, null=True)
    language = models.ForeignKey('languages.Language', verbose_name=_('language'), on_delete=models.SET_NULL, null=True)

    def clean(self):
        if not self.conference.topics.filter(id=self.topic_id).exists():
            raise exceptions.ValidationError(
                {'topic': f"{str(self.topic)} {_('is not a valid topic for the conference')} {self.conference.code}"}
            )

        if not self.conference.languages.filter(id=self.language_id).exists():
            raise exceptions.ValidationError(
                {'language': f"{str(self.language)} {_('is not a valid language for the conference')} {self.conference.code}"}
            )

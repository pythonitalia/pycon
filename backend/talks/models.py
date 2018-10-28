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
    helpers = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_('helpers'))

    track = models.ForeignKey('conferences.Track', verbose_name=_('track'), on_delete=models.SET_NULL, null=True)

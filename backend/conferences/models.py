from django.db import models

from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeFramedModel, TimeStampedModel


class Conference(TimeStampedModel, TimeFramedModel):
    name = models.CharField(_('name'), max_length=100)
    code = models.CharField(_('code'), max_length=10, unique=True)
    slug = models.SlugField()

    def __str__(self):
        return f'{self.name} <{self.slug}>'

    class Meta:
        verbose_name = _('Conference')
        verbose_name_plural = _('Conferences')

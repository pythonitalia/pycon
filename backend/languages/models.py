from django.db import models

from django.utils.translation import ugettext_lazy as _


class Language(models.Model):
    name = models.CharField(_('iso name'), max_length=100)
    code = models.CharField(_('code'), unique=True, max_length=2)

    def __str__(self):
        return f'{self.name} ({self.code})'

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')

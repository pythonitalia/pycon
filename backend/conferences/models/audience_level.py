from django.db import models
from django.utils.translation import ugettext_lazy as _


class AudienceLevel(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Audience Level")
        verbose_name_plural = _("Audience Levels")

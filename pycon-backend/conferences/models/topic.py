from django.db import models
from django.utils.translation import gettext_lazy as _


class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")

from django.db import models
from model_utils.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _


class BadgeScan(TimeStampedModel):
    scanned_by_id = models.IntegerField(verbose_name=_("Scanned By"))
    badge_url = models.URLField(_("Badge URL"), max_length=2048)
    notes = models.TextField(_("Notes"), blank=True)

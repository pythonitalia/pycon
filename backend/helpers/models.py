from django.db import models
from django.utils.translation import gettext_lazy as _


class GeoLocalizedModel(models.Model):
    """
    An abstract base class model that provides ``latitude``,
    ``longitude`` and ``map link`` fields to add position to a model.
    """

    latitude = models.DecimalField(
        _("latitude"), max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        _("longitude"), max_digits=9, decimal_places=6, blank=True, null=True
    )
    map_link = models.URLField(_("map link"), blank=True)

    class Meta:
        abstract = True

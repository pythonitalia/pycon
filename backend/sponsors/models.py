from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from ordered_model.models import OrderedModel
from pycon.constants import COLORS

from .managers import SponsorLevelManager, SponsorManager


class SponsorLevel(OrderedModel):
    name = models.CharField(_("name"), max_length=20)
    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        verbose_name=_("conference"),
        related_name="sponsor_levels",
    )
    highlight_color = models.CharField(
        choices=COLORS, max_length=15, blank=True, verbose_name=_("highlight color")
    )

    objects = SponsorLevelManager()

    def __str__(self):
        return self.name

    class Meta(OrderedModel.Meta):
        unique_together = ["name", "conference"]


class Sponsor(TimeStampedModel, OrderedModel):
    name = models.CharField(_("name"), max_length=200)
    link = models.URLField(_("link"), blank=True)
    image = models.ImageField(_("image"), null=True, blank=True, upload_to="sponsors")
    level = models.ForeignKey(
        SponsorLevel,
        on_delete=models.CASCADE,
        verbose_name=_("level"),
        related_name="sponsors",
    )

    objects = SponsorManager()

    def __str__(self):
        return self.name

    class Meta(OrderedModel.Meta):
        pass

from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from ordered_model.models import OrderedModel

from pycon.constants import COLORS

from .managers import SponsorLevelManager, SponsorManager
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit


class Sponsor(TimeStampedModel, OrderedModel):
    name = models.CharField(_("name"), max_length=200)
    link = models.URLField(_("link"), blank=True)
    image = models.ImageField(_("image"), null=True, blank=True, upload_to="sponsors")
    image_optimized = ImageSpecField(
        source="image",
        processors=[ResizeToFit(800, 400)],
        format="PNG",
        options={"quality": 60},
    )

    objects = SponsorManager()

    def __str__(self):
        return self.name

    class Meta(OrderedModel.Meta):
        pass


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
    sponsors = models.ManyToManyField(
        Sponsor,
        verbose_name=_("sponsors"),
        related_name="levels",
    )
    objects = SponsorLevelManager()
    order_with_respect_to = "conference"

    def __str__(self):
        return self.name

    class Meta(OrderedModel.Meta):
        unique_together = ["name", "conference"]


class SponsorLead(TimeStampedModel):
    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        related_name="sponsor_leads",
    )
    fullname = models.CharField(max_length=500)
    email = models.EmailField()
    company = models.CharField(max_length=500)
    brochure_viewed = models.BooleanField(default=False)

from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from ordered_model.models import OrderedModel


class SponsorLevel(OrderedModel):
    name = models.CharField(_("name"), max_length=20)
    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        verbose_name=_("conference"),
        related_name="sponsor_levels",
    )

    class Meta(OrderedModel.Meta):
        unique_together = ["name", "conference"]


class Sponsor(TimeStampedModel):
    name = models.CharField(_("name"), max_length=200)
    link = models.URLField(_("link"), blank=True)
    image = models.ImageField(_("image"), null=True, blank=True, upload_to="sponsors")
    level = models.ForeignKey(
        SponsorLevel,
        on_delete=models.CASCADE,
        verbose_name=_("level"),
        related_name="sponsors",
    )

    def __str__(self):
        return self.name

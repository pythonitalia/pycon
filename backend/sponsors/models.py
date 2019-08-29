from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


class Sponsor(TimeStampedModel):
    name = models.CharField(_("name"), max_length=200)
    level = models.CharField(_("level"), max_length=20)
    link = models.URLField(_("published"), blank=True)
    image = models.ImageField(_("image"), null=True, blank=True, upload_to="sponsors")
    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        verbose_name=_("conference"),
        related_name="sponsors",
    )

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ["name", "conference"]

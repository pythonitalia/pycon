from django.db import models
from django.utils.translation import ugettext_lazy as _
from helpers.models import GeoLocalizedModel
from i18n.fields import I18nCharField, I18nTextField
from model_utils.models import TimeFramedModel, TimeStampedModel


class Event(GeoLocalizedModel, TimeFramedModel, TimeStampedModel):
    title = I18nCharField(_("title"), blank=False)
    slug = I18nCharField(_("slug"), blank=False)
    content = I18nTextField(_("content"), blank=False)
    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        verbose_name=_("conference"),
        related_name="events",
    )
    image = models.ImageField(_("image"), null=True, blank=True, upload_to="events")

    def __str__(self):
        return f"{self.title} ({self.conference.name})"

    class Meta:
        unique_together = ["slug", "conference"]
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from pycon.constants import COLORS


class Keynote(TimeStampedModel):
    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        verbose_name=_("conference"),
        related_name="keynotes",
        null=False,
    )
    keynote_title = models.CharField(
        _("keynote title"), blank=False, max_length=512, default=""
    )
    keynote_description = models.TextField(
        _("keynote description"), blank=False, default=""
    )
    highlight_color = models.CharField(
        choices=COLORS, max_length=15, blank=True, verbose_name=_("highlight color")
    )

    def __str__(self) -> str:
        return f"{self.keynote_title} at {self.conference.code}"

    class Meta:
        verbose_name = _("Keynote")
        verbose_name_plural = _("Keynotes")


class KeynoteSpeaker(TimeStampedModel):
    keynote = models.ForeignKey(
        "conferences.Keynote",
        on_delete=models.CASCADE,
        verbose_name=_("keynote"),
        related_name="speakers",
        null=False,
    )

    name = models.CharField(
        _("fullname"),
        max_length=512,
        blank=False,
    )
    photo = models.ImageField(_("photo"), null=False, blank=False, upload_to="keynotes")
    bio = models.TextField(
        _("bio"),
        blank=False,
    )
    pronouns = models.CharField(
        _("pronouns"),
        max_length=512,
    )
    twitter_handle = models.CharField(
        _("twitter handle"),
        max_length=1024,
        default="",
        blank=True,
    )
    instagram_handle = models.CharField(
        _("instagram handle"),
        max_length=1024,
        default="",
        blank=True,
    )
    website = models.URLField(_("website"), blank=True, default="", max_length=2049)

    class Meta:
        verbose_name = _("Keynote Speaker")
        verbose_name_plural = _("Keynote Speakers")

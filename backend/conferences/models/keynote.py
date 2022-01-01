import json

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from ordered_model.models import OrderedModel, OrderedModelManager

from i18n.fields import I18nCharField, I18nTextField
from pycon.constants import COLORS


class KeynoteManager(OrderedModelManager):
    def by_slug(self, slug):
        term = json.dumps(slug)

        filters = Q()

        for lang, __ in settings.LANGUAGES:
            filters |= Q(**{f"slug__{lang}": term})

        return self.get_queryset().filter(filters)


class Keynote(OrderedModel, TimeStampedModel):
    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        verbose_name=_("conference"),
        related_name="keynotes",
        null=False,
    )
    slug = I18nCharField(_("slug"), max_length=200, unique=True)
    title = I18nCharField(_("keynote title"), blank=False, max_length=512, default="")
    description = I18nTextField(_("keynote description"), blank=False, default="")
    topic = models.ForeignKey(
        "conferences.Topic",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        default=None,
    )
    order_with_respect_to = "conference"
    objects = KeynoteManager()

    def __str__(self) -> str:
        return f"{self.title} at {self.conference.code}"

    class Meta(OrderedModel.Meta):
        verbose_name = _("Keynote")
        verbose_name_plural = _("Keynotes")


class KeynoteSpeaker(TimeStampedModel, OrderedModel):
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
    bio = I18nTextField(
        _("bio"),
        blank=False,
    )
    pronouns = I18nCharField(
        _("pronouns"),
        max_length=512,
    )
    highlight_color = models.CharField(
        choices=COLORS, max_length=15, blank=True, verbose_name=_("highlight color")
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
    order_with_respect_to = "keynote"

    class Meta(OrderedModel.Meta):
        verbose_name = _("Keynote Speaker")
        verbose_name_plural = _("Keynote Speakers")

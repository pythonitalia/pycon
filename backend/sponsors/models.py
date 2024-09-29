from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from ordered_model.models import OrderedModel

from pycon.constants import COLORS


from helpers.models import GeoLocalizedModel
from i18n.fields import I18nCharField, I18nTextField

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
    name = models.CharField(_("name"), max_length=100)
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
        blank=True,
    )
    objects = SponsorLevelManager()
    order_with_respect_to = "conference"

    def __str__(self):
        return self.name

    class Meta(OrderedModel.Meta):
        unique_together = ["name", "conference"]


class SponsorLevelBenefit(TimeStampedModel):
    class Category(models.TextChoices):
        CONTENT = "content", _("Sponsored Content")
        BOOTH = "booth", _("Booth")
        PASSES = "passes", _("Conference Passes")
        BRAND = "brand", _("Brand Visibility")
        RECRUITING = "recruiting", _("Recruiting")
        ATTENDEE_INTERACTION = "attendee_interaction", _("Attendee Interaction")

    sponsor_level = models.ForeignKey(
        "sponsors.SponsorLevel",
        on_delete=models.CASCADE,
        related_name="benefits",
        verbose_name=_("sponsor level"),
    )
    name = I18nCharField(_("name"), max_length=100)
    category = models.CharField(_("category"), max_length=100, choices=Category.choices)
    value = I18nTextField(_("value"), blank=True)
    description = I18nTextField(_("description"), blank=True)


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
    consent_to_contact_via_email = models.BooleanField(default=False)


def get_upload_to(instance, filename):
    return f"conferences/{instance.code}/{filename}"


class SponsorBrochure(TimeStampedModel):
    conference = models.OneToOneField(
        "conferences.Conference",
        verbose_name=_("conference"),
        on_delete=models.CASCADE,
        related_name="sponsor_brochure",
    )

    stats_attendees = models.CharField(
        _("Previous year's attendees"), max_length=100, default="800+"
    )
    stats_speakers = models.CharField(
        _("Previous year's speakers"), max_length=100, default="100+"
    )
    stats_talks = models.CharField(
        _("Previous year's talks"), max_length=100, default="110+"
    )
    stats_unique_online_visitors = models.CharField(
        _("Unique online visitors"), max_length=100, default="10,000+"
    )
    stats_sponsors = models.CharField(
        _("Previous year's sponsors & partners"), max_length=100, default="40+"
    )
    stats_grants_given = models.CharField(
        _("Previous year's grants given"), max_length=100, default="30+"
    )
    stats_coffee = models.CharField(
        _("Previous year's coffee consumed"), max_length=100, default="6,000+"
    )

    introduction = I18nTextField(_("introduction"), blank=True)
    tags = models.TextField(_("tags"), blank=True)

    city_description = I18nTextField(_("city description"), blank=True)
    country_description = I18nTextField(_("country description"), blank=True)

    community = I18nTextField(_("community"), blank=True)

    why_sponsor_intro = I18nTextField(_("why sponsor intro"), blank=True)
    why_sponsor = I18nTextField(_("why sponsor"), blank=True)

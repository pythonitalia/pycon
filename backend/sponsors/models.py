from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from ordered_model.models import OrderedModel

from pycon.constants import COLORS

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
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2, default=0)
    slots = models.PositiveSmallIntegerField(
        default=0, help_text=_("0 means unlimited")
    )

    benefits = models.ManyToManyField(
        "SponsorBenefit",
        through="SponsorLevelBenefit",
        verbose_name=_("benefits"),
        blank=True,
        limit_choices_to={"conference": models.F("conference")},
    )

    def __str__(self):
        return self.name

    class Meta(OrderedModel.Meta):
        unique_together = ["name", "conference"]


class SponsorBenefit(TimeStampedModel):
    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        related_name="sponsor_benefits",
    )

    class Category(models.TextChoices):
        CONTENT = "content", _("Sponsored Content")
        BOOTH = "booth", _("Booth")
        PASSES = "passes", _("Conference Passes")
        BRAND = "brand", _("Brand Visibility")
        RECRUITING = "recruiting", _("Recruiting")
        ATTENDEE_INTERACTION = "attendee_interaction", _("Attendee Interaction")

    name = I18nCharField(_("name"), max_length=100)
    category = models.CharField(_("category"), max_length=100, choices=Category.choices)
    description = I18nTextField(_("description"), blank=True)

    class Meta:
        unique_together = ["name", "conference"]
        verbose_name = _("sponsor benefit")
        verbose_name_plural = _("sponsor benefits")

    def __str__(self):
        return f"{self.name} ({self.conference})"


class SponsorLevelBenefit(models.Model):
    sponsor_level = models.ForeignKey(
        SponsorLevel, on_delete=models.CASCADE, verbose_name=_("sponsor level")
    )
    benefit = models.ForeignKey(
        SponsorBenefit, on_delete=models.CASCADE, verbose_name=_("benefit")
    )
    value = I18nCharField(
        default="✓", help_text=_("Value of the benefit, e.g. number of passes")
    )

    class Meta:
        unique_together = ["sponsor_level", "benefit"]
        verbose_name = _("sponsor level benefit")
        verbose_name_plural = _("sponsor level benefits")

    def __str__(self):
        return f"{self.sponsor_level} - {self.benefit} ({self.value})"


class SponsorSpecialOption(models.Model):
    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        related_name="sponsor_special_options",
    )
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"))
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _("special option")
        verbose_name_plural = _("special options")
        unique_together = ["name", "conference"]

    def __str__(self):
        return f"{self.name} ({self.conference})"


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

from copy import copy

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from ordered_model.models import OrderedModel, OrderedModelManager


class JobListingManager(OrderedModelManager):
    def by_slug(self, slug):
        filters = Q()

        for lang, __ in settings.LANGUAGES:
            filters |= Q(**{f"slug__{lang}": slug})

        return self.get_queryset().filter(filters)


class JobListing(TimeStampedModel, OrderedModel):
    title = models.TextField(_("title"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=200, blank=True)
    company = models.CharField(_("company"), max_length=100)
    company_logo = models.ImageField(
        _("company logo"), null=True, blank=True, upload_to="job-listings"
    )
    description = models.TextField(_("description"), blank=True)
    apply_url = models.TextField(_("Where you can apply"), blank=True)
    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        verbose_name=_("conference"),
        related_name="job_listings",
        null=True,
    )

    objects = JobListingManager()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"[{self.company}] - {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = copy(self.title)
            self.slug.map(slugify)

        super().save(*args, **kwargs)

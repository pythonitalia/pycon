import json
from copy import copy

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from i18n.fields import I18nCharField, I18nTextField
from model_utils.models import TimeStampedModel


class JobListingManager(models.Manager):
    def by_slug(self, slug):
        term = json.dumps(slug)

        filters = Q()

        for lang, __ in settings.LANGUAGES:
            filters |= Q(**{f"slug__{lang}": term})

        return self.get_queryset().filter(filters)


class JobListing(TimeStampedModel):
    title = I18nCharField(_("title"), max_length=200)
    slug = I18nCharField(_("slug"), max_length=200, blank=True)
    company = models.CharField(_("company"), max_length=100)
    company_logo = models.ImageField(
        _("company logo"), null=True, blank=True, upload_to="job-listings"
    )
    description = I18nTextField(_("description"), blank=True)
    apply_url = models.URLField(_("URL where you can apply"), blank=True)

    objects = JobListingManager()

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return f"[{self.company}] - {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = copy(self.title)
            self.slug.map(slugify)

        super().save(*args, **kwargs)

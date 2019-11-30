import json
from copy import copy

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from i18n.fields import I18nCharField, I18nTextField
from model_utils.models import TimeStampedModel


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(published__lte=timezone.now())

    def by_slug(self, slug):
        term = json.dumps(slug)

        filters = Q()

        for lang, __ in settings.LANGUAGES:
            filters |= Q(**{f"slug__{lang}": term})

        return self.get_queryset().filter(filters)


class Post(TimeStampedModel):
    author = models.ForeignKey("users.User", on_delete=models.CASCADE)
    title = I18nCharField(_("title"), max_length=200)
    slug = I18nCharField(_("slug"), max_length=200, blank=True)
    content = I18nTextField(_("content"), blank=True)
    excerpt = I18nTextField(_("excerpt"), blank=False)
    published = models.DateTimeField(_("published"), default=timezone.now)
    image = models.ImageField(_("image"), null=True, blank=True, upload_to="blog")

    objects = models.Manager()
    published_posts = PostManager()

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = copy(self.title)
            self.slug.map(slugify)

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-published"]

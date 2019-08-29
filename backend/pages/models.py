from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


class PageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(published=True)


class Page(TimeStampedModel):
    title = models.CharField(_("title"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=200, blank=True)
    content = models.TextField(_("content"), blank=False)
    published = models.BooleanField(_("published"), default=False)
    image = models.ImageField(_("image"), null=True, blank=True, upload_to="pages")
    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        verbose_name=_("conference"),
        related_name="pages",
    )

    objects = models.Manager()
    published_pages = PageManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-published"]
        unique_together = ["slug", "conference"]

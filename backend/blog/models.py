from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.utils import timezone
from model_utils.models import TimeStampedModel


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(published__lte=timezone.now())


class Post(TimeStampedModel):
    author = models.ForeignKey("users.User", on_delete=models.CASCADE)
    title = models.CharField(_("title"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=200, unique=True, blank=True)
    excerpt = models.TextField(_("excerpt"), null=True)
    content = models.TextField(_("content"), null=True)
    published = models.DateTimeField(_("published"), default=timezone.now)
    image = models.ImageField(_("image"), null=True, blank=True, upload_to="blog")

    objects = models.Manager()
    published_posts = PostManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-published"]

from django.db import models
from model_utils.models import TimeStampedModel


class Organizer(TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name} ({self.slug})"

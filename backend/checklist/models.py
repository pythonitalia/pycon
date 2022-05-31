from django.db import models
from model_utils.models import TimeStampedModel
from ordered_model.models import OrderedModel


class ChecklistItem(OrderedModel, TimeStampedModel):
    text = models.TextField("text", blank=False)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Checklist item"
        verbose_name_plural = "Checklist items"
        ordering = ("order",)

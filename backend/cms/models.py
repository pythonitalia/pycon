from django.db import models
from django.utils.translation import ugettext_lazy as _
from i18n.fields import I18nTextField
from model_utils.models import TimeStampedModel


class GenericCopy(TimeStampedModel):
    key = models.SlugField(_("slug"), max_length=200)
    content = I18nTextField(_("content"), blank=False)
    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        verbose_name=_("conference"),
        related_name="copy",
    )

    def __str__(self):
        return f"{self.key} ({self.conference.name})"

    class Meta:
        unique_together = ["key", "conference"]
        verbose_name = _("Generic Copy")
        verbose_name_plural = _("Generic Copy")


class FAQ(TimeStampedModel):
    question = I18nTextField(_("question"), blank=False)
    answer = I18nTextField(_("answer"), blank=False)
    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        verbose_name=_("conference"),
        related_name="faqs",
    )

    def __str__(self):
        return f"{self.question} ({self.conference.name})"

    class Meta:
        unique_together = ["question", "conference"]
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")

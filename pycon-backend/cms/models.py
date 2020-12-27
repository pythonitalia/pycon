from django.db import models
from django.utils.translation import gettext_lazy as _
from i18n.fields import I18nTextField
from model_utils.models import TimeStampedModel
from ordered_model.models import OrderedModel


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


class Menu(TimeStampedModel):
    identifier = models.SlugField(_("identifier"))
    title = I18nTextField(_("title"), blank=False)
    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        verbose_name=_("conference"),
        related_name="menus",
    )

    def __str__(self):
        return f"{self.identifier} ({self.conference.name})"

    class Meta:
        unique_together = ["identifier", "conference"]


class MenuLink(OrderedModel, TimeStampedModel):
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, verbose_name=_("menu"), related_name="links"
    )
    title = I18nTextField(_("title"), blank=False)
    href = I18nTextField(_("Link url"), blank=True)
    is_primary = models.BooleanField(_("Is primary"), default=False)
    page = models.ForeignKey(
        "pages.Page",
        on_delete=models.CASCADE,
        verbose_name=_("page"),
        related_name="links",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.title} ({self.menu})"

from enum import Enum

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeFramedModel

from i18n.fields import I18nCharField, I18nTextField


class DeadlineStatus(Enum):
    IN_THE_FUTURE = "in-the-future"
    HAPPENING_NOW = "happening-now"
    IN_THE_PAST = "in-the-past"


class Deadline(TimeFramedModel):
    TYPES = Choices(
        ("cfp", _("Call for proposal")),
        ("voting", _("Voting")),
        ("refund", _("Ticket refund")),
        ("grants", _("Grants")),
        ("custom", _("Custom deadline")),
    )

    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        verbose_name=_("conference"),
        related_name="deadlines",
    )

    name = I18nCharField(_("name"), max_length=100)
    description = I18nTextField(_("description"), blank=True, null=True)
    type = models.CharField(_("type"), choices=TYPES, max_length=10)

    def __str__(self):
        return f"{self.type} ({self.name}) <{self.conference.code}>"

    @property
    def status(self) -> DeadlineStatus:
        now = timezone.now()

        if now >= self.start and now <= self.end:
            return DeadlineStatus.HAPPENING_NOW

        if self.start > now:
            return DeadlineStatus.IN_THE_FUTURE

        return DeadlineStatus.IN_THE_PAST

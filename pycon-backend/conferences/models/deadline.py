from django.core import exceptions
from django.db import models
from django.utils.translation import gettext_lazy as _
from i18n.fields import I18nCharField, I18nTextField
from model_utils import Choices
from model_utils.models import TimeFramedModel


class Deadline(TimeFramedModel):
    TYPES = Choices(
        ("cfp", _("Call for proposal")),
        ("voting", _("Voting")),
        ("refund", _("Ticket refund")),
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

    def clean(self):
        super().clean()

        if self.start > self.end:
            raise exceptions.ValidationError(_("Start date cannot be after end"))

        if self.type != Deadline.TYPES.custom:
            if (
                Deadline.objects.filter(conference=self.conference, type=self.type)
                .exclude(id=self.id)
                .exists()
            ):
                raise exceptions.ValidationError(
                    _("You can only have one deadline of type %(type)s")
                    % {"type": self.type}
                )

    def __str__(self):
        return f"{self.type} ({self.name}) <{self.conference.code}>"

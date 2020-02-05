from conferences.models import Conference
from django.conf import settings
from django.contrib.postgres.fields.jsonb import JSONField
from django.core import exceptions
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeFramedModel, TimeStampedModel
from pycon.constants import COLORS
from submissions.models import Submission


class Day(models.Model):
    day = models.DateField()
    conference = models.ForeignKey(
        Conference,
        on_delete=models.CASCADE,
        verbose_name=_("conference"),
        related_name="days",
    )
    schedule_configuration = JSONField(default=list)

    def __str__(self):
        return f"{self.day.isoformat()} at {self.conference}"


class Room(models.Model):
    name = models.CharField(_("name"), max_length=100)
    conference = models.ForeignKey(
        Conference,
        on_delete=models.CASCADE,
        verbose_name=_("conference"),
        related_name="rooms",
    )

    def __str__(self):
        return f"{self.name} at {self.conference}"

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")


class ScheduleItem(TimeFramedModel, TimeStampedModel):
    TYPES = Choices(
        ("submission", _("Submission")),
        ("keynote", _("Keynote")),
        ("custom", _("Custom")),
    )

    conference = models.ForeignKey(
        Conference,
        on_delete=models.CASCADE,
        verbose_name=_("conference"),
        related_name="schedule_items",
    )

    title = models.CharField(_("title"), max_length=100, blank=True)
    slug = models.CharField(_("slug"), max_length=100, blank=True)
    description = models.TextField(_("description"), blank=True)

    type = models.CharField(choices=TYPES, max_length=10, verbose_name=_("type"))
    highlight_color = models.CharField(
        choices=COLORS, max_length=15, blank=True, verbose_name=_("highlight color")
    )

    rooms = models.ManyToManyField(Room, related_name="talks", verbose_name=_("rooms"))

    submission = models.ForeignKey(
        Submission,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("submission"),
    )
    image = models.ImageField(
        _("image"), null=True, blank=True, upload_to="schedule_items"
    )

    additional_speakers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_("speakers"), blank=True
    )

    def clean(self):
        if self.type == ScheduleItem.TYPES.submission and not self.submission:
            raise exceptions.ValidationError(
                {
                    "submission": _(
                        "You have to specify a submission when "
                        "using the type `submission`"
                    )
                }
            )

        if self.type == ScheduleItem.TYPES.custom and not self.title:
            raise exceptions.ValidationError(
                {"title": _("You have to specify a title when using the type `custom`")}
            )

    def __str__(self):
        title = (
            self.submission.title
            if self.type == ScheduleItem.TYPES.submission
            else self.title
        )
        return f"{self.conference.name}. Start: {self.start} End: {self.end}. {title}"

    class Meta:
        verbose_name = _("Schedule item")
        verbose_name_plural = _("Schedule items")
        unique_together = ("slug", "conference")

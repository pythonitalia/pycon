from conferences.models import Conference
from django.conf import settings
from django.core import exceptions
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel
from ordered_model.models import OrderedModel
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

    def __str__(self):
        return f"{self.day.isoformat()} at {self.conference}"


class Slot(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name="slots")
    hour = models.TimeField()
    duration = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.day} - {self.hour}"

    class Meta:
        ordering = ["hour"]


class Room(OrderedModel):
    TYPES = Choices(("talk", _("Talk room")), ("training", _("Training room")))

    name = models.CharField(_("name"), max_length=100)
    conference = models.ForeignKey(
        Conference,
        on_delete=models.CASCADE,
        verbose_name=_("conference"),
        related_name="rooms",
    )
    type = models.CharField(_("type"), choices=TYPES, max_length=10, default=TYPES.talk)

    def __str__(self):
        return f"{self.name} at {self.conference}"

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")


class ScheduleItem(TimeStampedModel):
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
    slug = models.CharField(_("slug"), max_length=100, blank=True, null=True)
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
        related_name="schedule_items",
    )
    image = models.ImageField(
        _("image"), null=True, blank=True, upload_to="schedule_items"
    )

    slot = models.ForeignKey(
        Slot, blank=True, null=True, related_name="items", on_delete=models.PROTECT
    )
    duration = models.PositiveIntegerField(null=True, blank=True)

    additional_speakers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_("speakers"), blank=True
    )
    language = models.ForeignKey(
        "languages.Language",
        verbose_name=_("language"),
        related_name="+",
        on_delete=models.PROTECT,
    )

    @cached_property
    def speakers(self):
        speakers = set(self.additional_speakers.all())

        if self.submission:
            speakers.add(self.submission.speaker)

        return speakers

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

    def save(self, **kwargs):
        if self.submission and not self.title:
            self.title = self.submission.title

        # see: https://stackoverflow.com/q/454436/169274
        self.slug = self.slug or None

        if "update_fields" in kwargs:
            kwargs["update_fields"].append("slug")
            kwargs["update_fields"].append("title")

        super().save(**kwargs)

    class Meta:
        verbose_name = _("Schedule item")
        verbose_name_plural = _("Schedule items")
        unique_together = ("slug", "conference")

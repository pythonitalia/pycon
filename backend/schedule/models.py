from collections import namedtuple

from django.core import exceptions
from django.db import models
from django.db.models import Case, When
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel
from ordered_model.models import OrderedModel

from conferences.models import Conference
from helpers.unique_slugify import unique_slugify
from pycon.constants import COLORS
from submissions.models import Submission

SpeakerEntity = namedtuple("SpeakerEntity", ("id",))


class Room(models.Model):
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


class Day(models.Model):
    day = models.DateField()
    conference = models.ForeignKey(
        Conference,
        on_delete=models.CASCADE,
        verbose_name=_("conference"),
        related_name="days",
    )

    def ordered_rooms(self):
        added_rooms = self.added_rooms.all()
        ordered_pks = added_rooms.values_list("room_id", flat=True)
        orders = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ordered_pks)])
        rooms = Room.objects.filter(id__in=ordered_pks).order_by(orders)
        return rooms

    def __str__(self):
        return f"{self.day.isoformat()} at {self.conference}"


class DayRoomThroughModel(OrderedModel):
    day = models.ForeignKey(
        Day,
        on_delete=models.CASCADE,
        verbose_name=_("day"),
        related_name="added_rooms",
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        verbose_name=_("room"),
    )
    order_with_respect_to = "day"

    class Meta:
        ordering = (
            "day",
            "order",
        )
        verbose_name = _("Day - Room")
        verbose_name_plural = _("Day - Rooms")


class Slot(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name="slots")
    hour = models.TimeField()
    duration = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.day} - {self.hour}"

    class Meta:
        ordering = ["hour"]


class ScheduleItem(TimeStampedModel):
    TYPES = Choices(
        ("submission", _("Submission")),
        ("training", _("Training")),
        ("keynote", _("Keynote")),
        ("custom", _("Custom")),
    )

    STATUS = Choices(
        ("confirmed", _("Confirmed")),
        ("maybe", _("Maybe")),
        ("waiting_confirmation", _("Waiting confirmation")),
        ("cancelled", _("Cancelled")),
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
    status = models.CharField(
        choices=STATUS,
        max_length=25,
        verbose_name=_("status"),
        default=STATUS.waiting_confirmation,
    )
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

    language = models.ForeignKey(
        "languages.Language",
        verbose_name=_("language"),
        related_name="+",
        on_delete=models.PROTECT,
    )

    audience_level = models.ForeignKey(
        "conferences.AudienceLevel",
        verbose_name=_("audience level"),
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )

    @cached_property
    def speakers(self):
        speakers = set(
            [
                SpeakerEntity(speaker.user_id)
                for speaker in self.additional_speakers.all()
            ]
        )

        if self.submission:
            speakers.add(SpeakerEntity(self.submission.speaker_id))

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

        if not self.slug:
            unique_slugify(self, self.title)

        if "update_fields" in kwargs:
            kwargs["update_fields"].append("slug")
            kwargs["update_fields"].append("title")

        super().save(**kwargs)

    class Meta:
        verbose_name = _("Schedule item")
        verbose_name_plural = _("Schedule items")
        unique_together = ("slug", "conference")


class ScheduleItemAdditionalSpeaker(models.Model):
    scheduleitem = models.ForeignKey(
        ScheduleItem,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name=_("schedule item"),
        related_name="additional_speakers",
    )
    user_id = models.IntegerField(verbose_name=_("user"))

    class Meta:
        verbose_name = _("Schedule item additional speaker")
        verbose_name_plural = _("Schedule item additional speakers")
        unique_together = ("user_id", "scheduleitem")
        db_table = "schedule_scheduleitem_additional_speakers"

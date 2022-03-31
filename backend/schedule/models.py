from dataclasses import dataclass
from typing import Optional

from django.core import exceptions
from django.db import models
from django.db.models import Case, When
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel
from ordered_model.models import OrderedModel

from conferences.models import Conference, Keynote
from helpers.unique_slugify import unique_slugify
from pycon.constants import COLORS
from submissions.models import Submission


@dataclass
class SpeakerEntity:
    id: Optional[str] = None
    full_name: str = ""


class Room(models.Model):
    TYPES = Choices(("talk", _("Talk room")), ("training", _("Training room")))

    name = models.CharField(_("name"), max_length=100)
    type = models.CharField(_("type"), choices=TYPES, max_length=10, default=TYPES.talk)

    def __str__(self):
        return self.name

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
        return f"[{self.day.conference.name}] {self.day.day} - {self.hour}"

    class Meta:
        ordering = ["hour"]


class ScheduleItem(TimeStampedModel):
    TYPES = Choices(
        ("submission", _("Submission")),
        ("talk", _("Talk")),
        ("training", _("Training")),
        ("keynote", _("Keynote")),
        ("custom", _("Custom")),
    )

    STATUS = Choices(
        ("confirmed", _("Confirmed")),
        ("maybe", _("Maybe")),
        ("rejected", _("Speaker Rejected")),
        ("cant_attend", _("Speaker can't attend anymore")),
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
    keynote = models.ForeignKey(
        Keynote,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("keynote"),
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

    speaker_invitation_notes = models.TextField(
        verbose_name=_("Speaker invitation notes"),
        default="",
        blank=True,
    )
    speaker_invitation_sent_at = models.DateTimeField(
        _("speaker invitation sent at"), null=True, blank=True
    )

    attendees_total_capacity = models.PositiveIntegerField(
        verbose_name=_("Attendees total capacity"),
        help_text=_(
            "Maximum capacity for this event. Leave blank to not limit attendees."
        ),
        null=True,
        blank=True,
    )

    exclude_from_voucher_generation = models.BooleanField(
        help_text=_(
            "If true this speaker will not be included in the voucher generation."
        ),
        default=False,
    )

    @cached_property
    def speakers(self):
        speakers = [
            SpeakerEntity(id=speaker.user_id)
            for speaker in self.additional_speakers.all()
        ]

        if self.submission_id:
            speakers.append(SpeakerEntity(id=self.submission.speaker_id))

        if self.keynote_id:
            for speaker_keynote in self.keynote.speakers.all():
                speakers.append(SpeakerEntity(full_name=speaker_keynote.name))

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
        if self.submission_id and not self.title:
            self.title = self.submission.title

        if self.keynote_id and not self.title:
            self.title = self.keynote.title.localize("em")

        if not self.slug:
            unique_slugify(self, self.title)

        if "update_fields" in kwargs:
            kwargs["update_fields"].append("slug")
            kwargs["update_fields"].append("title")

        super().save(**kwargs)

    def get_invitation_admin_url(self):
        return reverse(
            "admin:schedule_scheduleiteminvitation_change",
            args=(self.pk,),
        )

    def get_admin_url(self):
        return reverse(
            "admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name),
            args=(self.pk,),
        )

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


class ScheduleItemAttendee(TimeStampedModel):
    user_id = models.IntegerField(verbose_name=_("user"))
    schedule_item = models.ForeignKey(
        ScheduleItem,
        on_delete=models.CASCADE,
        verbose_name=_("schedule item"),
        related_name="attendees",
    )

    class Meta:
        unique_together = (
            "user_id",
            "schedule_item",
        )


class ScheduleItemInvitation(ScheduleItem):
    class Meta:
        proxy = True
        verbose_name = _("Schedule invitation")
        verbose_name_plural = _("Schedule invitations")

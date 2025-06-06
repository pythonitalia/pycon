from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional
from conferences.querysets import ConferenceQuerySetMixin

from django.core import exceptions
from django.db import models
from django.db.models import Case, When
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel
from ordered_model.models import OrderedModel
from django.db.models import QuerySet

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


class DayQuerySet(ConferenceQuerySetMixin, models.QuerySet):
    pass


class Day(models.Model):
    day = models.DateField()
    conference = models.ForeignKey(
        Conference,
        on_delete=models.CASCADE,
        verbose_name=_("conference"),
        related_name="days",
    )
    objects = DayQuerySet().as_manager()

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
    streaming_url = models.URLField(_("Streaming URL"), blank=True, default="")
    slido_url = models.URLField(_("Sli.do URL"), blank=True, default="")

    class Meta:
        ordering = (
            "day",
            "order",
        )
        verbose_name = _("Day - Room")
        verbose_name_plural = _("Day - Rooms")


class SlotQuerySet(QuerySet, ConferenceQuerySetMixin):
    pass


class Slot(models.Model):
    conference_reference = "day__conference"

    TYPES = Choices(
        # Type of slot where something is happening in the conference
        ("default", _("Default")),
        # Free time, that can used to change rooms
        # or represent time between social events
        ("free_time", _("Free Time")),
        ("break", _("Break")),
    )

    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name="slots")
    hour = models.TimeField()
    duration = models.PositiveSmallIntegerField()
    type = models.CharField(
        choices=TYPES, max_length=100, verbose_name=_("type"), default=TYPES.default
    )

    objects = SlotQuerySet().as_manager()

    def __str__(self):
        return f"[{self.day.conference.name}] {self.day.day} - {self.hour}"

    class Meta:
        ordering = ["hour"]


class ScheduleItemSentForVideoUploadQuerySet(QuerySet):
    def to_upload(self):
        return self.filter(status=ScheduleItemSentForVideoUpload.Status.pending)


class ScheduleItemSentForVideoUpload(TimeStampedModel):
    class Status(models.TextChoices):
        pending = "pending", _("Pending")
        processing = "processing", _("Processing")
        completed = "completed", _("Completed")
        failed = "failed", _("Failed")

    status = models.CharField(
        _("Status"),
        max_length=100,
        choices=Status.choices,
        default=Status.pending,
    )
    schedule_item = models.OneToOneField(
        "schedule.ScheduleItem",
        on_delete=models.CASCADE,
    )
    attempts = models.PositiveIntegerField(_("Video upload attempts"), default=0)
    last_attempt_at = models.DateTimeField(_("Last attempt at"), null=True, blank=True)
    video_uploaded = models.BooleanField(_("Video uploaded"), default=False)
    thumbnail_uploaded = models.BooleanField(_("Thumbnail uploaded"), default=False)
    failed_reason = models.TextField(
        _("Failed reason"),
        blank=True,
        default="",
    )
    objects = ScheduleItemSentForVideoUploadQuerySet().as_manager()

    @property
    def is_pending(self):
        return self.status == self.Status.pending


class ScheduleItemQuerySet(QuerySet, ConferenceQuerySetMixin):
    pass


class ScheduleItem(TimeStampedModel):
    TYPES = Choices(
        ("submission", _("Submission")),
        ("talk", _("Talk")),
        ("training", _("Training")),
        ("keynote", _("Keynote")),
        ("panel", _("Panel")),
        ("registration", _("Registration")),
        ("announcements", _("Announcements")),
        ("recruiting", _("Recruiting")),
        ("break", _("Break")),
        ("social", _("Social")),
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

    type = models.CharField(choices=TYPES, max_length=100, verbose_name=_("type"))
    status = models.CharField(
        choices=STATUS,
        max_length=25,
        verbose_name=_("status"),
        default=STATUS.waiting_confirmation,
    )
    highlight_color = models.CharField(
        choices=COLORS, max_length=15, blank=True, verbose_name=_("highlight color")
    )

    rooms = models.ManyToManyField(
        Room, related_name="talks", verbose_name=_("rooms"), blank=True
    )
    livestreaming_room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("livestreaming room"),
        related_name="livestreaming_talks",
    )

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
    link_to = models.CharField(_("link to"), blank=True, default="", max_length=1024)

    talk_manager = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("talk manager"),
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

    slido_url = models.URLField(_("Sli.do URL"), blank=True, default="")

    video_uploaded_path = models.CharField(
        _("path in the storage where the video file is uploaded"),
        max_length=1024,
        blank=True,
        default="",
    )
    youtube_video_id = models.CharField(
        _("Youtube video ID"), max_length=1024, blank=True, default=""
    )

    plain_thread_id = models.CharField(
        _("Plain threadID"),
        max_length=50,
        null=True,
        blank=True,
    )

    objects = ScheduleItemQuerySet().as_manager()

    @cached_property
    def speakers(self):
        speakers = []

        if self.submission_id:
            speakers.append(self.submission.speaker)

        if self.keynote_id:
            for speaker_keynote in self.keynote.speakers.order_by("id").all():
                speakers.append(speaker_keynote.user)

        speakers.extend(
            [speaker.user for speaker in self.additional_speakers.order_by("id").all()]
        )
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
            self.title = self.submission.title.localize(self.language.code)

        if self.keynote_id and not self.title:
            self.title = self.keynote.title.localize(self.language.code)

        if not self.slug:
            unique_slugify(self, self.title)

        if "update_fields" in kwargs:
            kwargs["update_fields"].append("slug")
            kwargs["update_fields"].append("title")

        super().save(**kwargs)

    @property
    def start(self):
        hour_slot = self.slot.hour
        day = self.slot.day.day
        return datetime.combine(day, hour_slot)

    @property
    def end(self):
        hour_slot = self.slot.hour
        day = self.slot.day.day
        start = datetime.combine(day, hour_slot)
        duration = self.duration or self.slot.duration
        return start + timedelta(minutes=duration)

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

    def __str__(self):
        return self.title

    @property
    def abstract(self):
        language_code = self.language.code

        if self.submission_id:
            return self.submission.abstract.localize(language_code)

        if self.keynote_id:
            return self.keynote.description.localize(language_code)

        return self.description

    @property
    def elevator_pitch(self):
        language_code = self.language.code

        if self.submission_id:
            return self.submission.elevator_pitch.localize(language_code)

        return ""

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
    user = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        verbose_name=_("user"),
        related_name="+",
    )

    class Meta:
        verbose_name = _("Schedule item additional speaker")
        verbose_name_plural = _("Schedule item additional speakers")
        unique_together = ("user", "scheduleitem")
        db_table = "schedule_scheduleitem_additional_speakers"


class ScheduleItemAttendee(TimeStampedModel):
    schedule_item = models.ForeignKey(
        ScheduleItem,
        on_delete=models.CASCADE,
        verbose_name=_("schedule item"),
        related_name="attendees",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name=_("user"),
        related_name="+",
    )

    class Meta:
        unique_together = (
            "user",
            "schedule_item",
        )


class ScheduleItemInvitation(ScheduleItem):
    class Meta:
        proxy = True
        verbose_name = _("Schedule invitation")
        verbose_name_plural = _("Schedule invitations")


class ScheduleItemStarQuerySet(ConferenceQuerySetMixin, QuerySet):
    def of_user(self, user):
        return self.filter(user=user)


class ScheduleItemStar(TimeStampedModel):
    conference_reference = "schedule_item__conference"

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name=_("user"),
        related_name="+",
    )
    schedule_item = models.ForeignKey(
        ScheduleItem,
        on_delete=models.CASCADE,
        verbose_name=_("schedule item"),
        related_name="stars",
    )

    objects = ScheduleItemStarQuerySet().as_manager()

    class Meta:
        unique_together = (
            "user",
            "schedule_item",
        )

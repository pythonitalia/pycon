from django.core import exceptions
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel

from api.helpers.ids import encode_hashid
from i18n.fields import I18nCharField, I18nTextField

from .querysets import SubmissionQuerySet


class SubmissionTag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Submission(TimeStampedModel):
    SPEAKER_LEVELS = Choices(
        ("new", _("New speaker")),
        ("intermediate", _("Intermediate experience")),
        ("experienced", _("Experienced")),
    )

    STATUS = Choices(
        ("proposed", _("Proposed")),
        ("accepted", _("Accepted")),
        ("waiting_list", _("Waiting list")),
        ("rejected", _("Rejected")),
        ("cancelled", _("Cancelled")),
    )

    NON_CANCELLED_STATUSES = [
        STATUS.proposed,
        STATUS.accepted,
        STATUS.waiting_list,
        STATUS.rejected,
    ]

    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        verbose_name=_("conference"),
        related_name="submissions",
    )

    title = I18nCharField(_("title"))
    abstract = I18nTextField(_("abstract"))
    elevator_pitch = I18nTextField(_("elevator pitch"), default="", blank=True)
    slug = models.SlugField(_("slug"), max_length=200)
    notes = models.TextField(_("notes"), default="", blank=True, max_length=1000)
    short_social_summary = models.TextField(
        _("short social summary"), default="", blank=True, max_length=128
    )

    speaker_level = models.CharField(
        _("speaker level"), choices=SPEAKER_LEVELS, max_length=20
    )
    previous_talk_video = models.URLField(
        _("previous talk video"), blank=True, max_length=2049
    )

    speaker = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name=_("speaker"),
        related_name="+",
    )

    topic = models.ForeignKey(
        "conferences.Topic",
        verbose_name=_("topic"),
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )

    languages = models.ManyToManyField(
        "languages.Language", verbose_name=_("languages")
    )

    type = models.ForeignKey(
        "submissions.SubmissionType", verbose_name=_("type"), on_delete=models.PROTECT
    )

    duration = models.ForeignKey(
        "conferences.Duration", verbose_name=_("duration"), on_delete=models.PROTECT
    )

    audience_level = models.ForeignKey(
        "conferences.AudienceLevel",
        verbose_name=_("audience level"),
        on_delete=models.PROTECT,
    )

    tags = models.ManyToManyField("submissions.SubmissionTag", verbose_name=_("tags"))
    status = models.CharField(
        _("status"), choices=STATUS, max_length=20, default=STATUS.proposed
    )
    pending_status = models.CharField(
        _("pending status"), choices=STATUS, max_length=20, default="", blank=True
    )

    objects = SubmissionQuerySet().as_manager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_status = self.status

    @property
    def hashid(self):
        return encode_hashid(self.pk)

    def can_edit(self, request):
        return self.speaker_id == request.user.id

    def clean(self):
        if (
            self.topic_id
            and not self.conference.topics.filter(id=self.topic_id).exists()
        ):
            raise exceptions.ValidationError(
                {
                    "topic": _("%(topic)s is not a valid topic")
                    % {"topic": str(self.topic)}
                }
            )

        if (
            self.type_id
            and not self.conference.submission_types.filter(id=self.type_id).exists()
        ):
            raise exceptions.ValidationError(
                {
                    "type": _("%(submission_type)s is not an allowed submission type")
                    % {"submission_type": str(self.type)}
                }
            )

        if (
            self.duration_id
            and not self.conference.durations.filter(id=self.duration_id).exists()
        ):
            raise exceptions.ValidationError(
                {"duration": _(f"{str(self.duration)} is not an allowed duration type")}
            )

        if (
            self.duration_id
            and self.type_id
            and not self.duration.allowed_submission_types.filter(
                id=self.type_id
            ).exists()
        ):
            raise exceptions.ValidationError(
                {
                    "duration": _(
                        f"Duration {str(self.duration)} is not an allowed for "
                        f"the submission type {str(self.type)}"
                    )
                }
            )

        if (
            self.audience_level_id
            and not self.conference.audience_levels.filter(
                id=self.audience_level_id
            ).exists()
        ):
            raise exceptions.ValidationError(
                {
                    "audience_level": _(
                        "%(audience_level)s is not an allowed audience level"
                    )
                    % {"audience_level": str(self.audience_level)}
                }
            )

    def get_admin_url(self):
        return reverse(
            "admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name),
            args=(self.pk,),
        )

    def save(self, *args, **kwargs):
        update_fields = kwargs.get("update_fields", None)

        if not self.slug:
            self.slug = slugify(self.title.localize("en"))

            if update_fields:
                update_fields.append("slug")

        if self.pending_status == self._original_status:
            self.pending_status = self.status

            if update_fields:
                update_fields.append("pending_status")

        return super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.title} at Conference {self.conference.name} "
            f"<{self.conference.code}>"
        )


class ProposalMaterial(TimeStampedModel):
    proposal = models.ForeignKey(
        "submissions.Submission",
        on_delete=models.CASCADE,
        verbose_name=_("proposal"),
        related_name="materials",
    )

    name = models.CharField(_("name"), max_length=100)
    url = models.URLField(_("url"), max_length=2049, blank=True, null=True)
    file = models.ForeignKey(
        "files_upload.File",
        on_delete=models.CASCADE,
        verbose_name=_("file"),
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.name} for {self.proposal.title}"


class SubmissionType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class SubmissionComment(TimeStampedModel):
    submission = models.ForeignKey(
        "submissions.Submission",
        on_delete=models.CASCADE,
        verbose_name=_("submission"),
        related_name="comments",
    )

    author = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name=_("author"),
        related_name="+",
    )

    text = models.CharField(_("text"), max_length=500)

    def get_admin_url(self):
        return reverse(
            "admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name),
            args=(self.pk,),
        )

    def __str__(self):
        return f"{self.author_id} {self.submission.title}"

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")


class SubmissionConfirmPendingStatusProxy(Submission):
    class Meta:
        proxy = True
        verbose_name = _("Submission Confirm Pending Status")
        verbose_name_plural = _("Submissions Confirm Pending Status")

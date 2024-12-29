from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeFramedModel, TimeStampedModel
from timezone_field import TimeZoneField

from helpers.models import GeoLocalizedModel
from i18n.fields import I18nCharField, I18nTextField

from .deadline import Deadline, DeadlineStatus


def get_upload_to(instance, filename):
    return f"conferences/{instance.code}/{filename}"


class Conference(GeoLocalizedModel, TimeFramedModel, TimeStampedModel):
    organizer = models.ForeignKey(
        "organizers.Organizer",
        verbose_name=_("organizer"),
        on_delete=models.PROTECT,
        related_name="conferences",
        null=True,
    )

    name = I18nCharField(_("name"), max_length=100)
    code = models.CharField(_("code"), max_length=100, unique=True)
    timezone = TimeZoneField()
    logo = models.ImageField(_("logo"), upload_to=get_upload_to, blank=True)
    location = models.TextField(_("location"), max_length=1024, blank=True)

    topics = models.ManyToManyField(
        "conferences.Topic", verbose_name=_("topics"), blank=True
    )
    languages = models.ManyToManyField(
        "languages.Language", verbose_name=_("languages"), blank=True
    )
    audience_levels = models.ManyToManyField(
        "conferences.AudienceLevel", verbose_name=_("audience levels"), blank=True
    )
    submission_types = models.ManyToManyField(
        "submissions.SubmissionType", verbose_name=_("submission types"), blank=True
    )
    proposal_tags = models.ManyToManyField(
        "submissions.SubmissionTag", verbose_name=_("proposal tags"), blank=True
    )

    pretix_organizer_id = models.CharField(
        _("pretix organizer id"), max_length=200, blank=True, default=""
    )
    pretix_event_id = models.CharField(
        _("pretix event id"), max_length=200, blank=True, default=""
    )
    pretix_event_url = models.URLField(_("pretix event url"), blank=True, default="")

    pretix_conference_voucher_quota_id = models.IntegerField(
        _("Pretix speaker voucher quota id"),
        blank=True,
        null=True,
    )

    introduction = I18nTextField(_("introduction"), blank=False)

    slack_new_proposal_channel_id = models.CharField(
        _("New proposal Slack channel ID for notification"),
        max_length=255,
        blank=True,
        default="",
    )
    slack_new_grant_reply_channel_id = models.CharField(
        _("New grant reply Slack channel ID for notification"),
        max_length=255,
        blank=True,
        default="",
    )
    slack_speaker_invitation_answer_channel_id = models.CharField(
        _("New speaker invitation answer Slack channel ID for notification"),
        max_length=255,
        blank=True,
        default="",
    )
    slack_new_sponsor_lead_channel_id = models.CharField(
        _("New sponsor lead Slack channel ID for notification"),
        max_length=255,
        blank=True,
        default="",
    )

    grants_default_ticket_amount = models.DecimalField(
        verbose_name=_("grants default ticket amount"),
        null=True,
        blank=True,
        max_digits=6,
        decimal_places=2,
        default=None,
    )
    grants_default_accommodation_amount = models.DecimalField(
        verbose_name=_("grants default accommodation amount"),
        null=True,
        blank=True,
        max_digits=6,
        decimal_places=2,
        default=None,
    )
    grants_default_travel_from_italy_amount = models.DecimalField(
        verbose_name=_("grants default travel from Italy amount"),
        null=True,
        blank=True,
        max_digits=6,
        decimal_places=2,
        default=None,
    )
    grants_default_travel_from_europe_amount = models.DecimalField(
        verbose_name=_("grants default travel from Europe amount"),
        null=True,
        blank=True,
        max_digits=6,
        decimal_places=2,
        default=None,
    )
    grants_default_travel_from_extra_eu_amount = models.DecimalField(
        verbose_name=_("grants default travel from Extra EU amount"),
        null=True,
        blank=True,
        max_digits=6,
        decimal_places=2,
        default=None,
    )

    video_title_template = models.TextField(
        default="",
        blank=True,
    )
    video_description_template = models.TextField(
        default="",
        blank=True,
    )

    youtube_video_bottom_text = models.TextField(
        default="",
        blank=True,
    )

    def get_slack_oauth_token(self):
        return self.organizer.slack_oauth_bot_token

    @property
    def is_cfp_open(self):
        try:
            cfp_deadline = self.deadlines.get(type=Deadline.TYPES.cfp)

            now = timezone.now()
            return cfp_deadline.start <= now <= cfp_deadline.end
        except Deadline.DoesNotExist:
            return False

    @property
    def is_voting_open(self):
        try:
            voting_deadline = self.deadlines.get(type=Deadline.TYPES.voting)

            now = timezone.now()
            return voting_deadline.start <= now <= voting_deadline.end
        except Deadline.DoesNotExist:
            return False

    @cached_property
    def is_voting_closed(self):
        try:
            voting_deadline = self.deadlines.get(type=Deadline.TYPES.voting)

            now = timezone.now()
            return voting_deadline.end <= now
        except Deadline.DoesNotExist:
            return False

    @cached_property
    def is_grants_open(self):
        try:
            grants_deadline = self.deadlines.get(type=Deadline.TYPES.grants)

            return grants_deadline.status == DeadlineStatus.HAPPENING_NOW
        except Deadline.DoesNotExist:
            return False

    def is_deadline_active(self, deadline_type: str):
        try:
            deadline = self.deadlines.get(type=deadline_type)
            return deadline.status == DeadlineStatus.HAPPENING_NOW
        except Deadline.DoesNotExist:
            return False

    def __str__(self):
        return f"{self.name} <{self.code}>"

    class Meta:
        verbose_name = _("Conference")
        verbose_name_plural = _("Conferences")

from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from helpers.models import GeoLocalizedModel
from i18n.fields import I18nCharField, I18nTextField
from model_utils.models import TimeFramedModel, TimeStampedModel
from timezone_field import TimeZoneField

from .deadline import Deadline


class Conference(GeoLocalizedModel, TimeFramedModel, TimeStampedModel):
    name = I18nCharField(_("name"), max_length=100)
    code = models.CharField(_("code"), max_length=10, unique=True)
    timezone = TimeZoneField()

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

    pretix_organizer_id = models.CharField(
        _("pretix organizer id"), max_length=200, blank=True, default=""
    )
    pretix_event_id = models.CharField(
        _("pretix event id"), max_length=200, blank=True, default=""
    )
    pretix_event_url = models.URLField(_("pretix event url"), blank=True, default="")

    pretix_hotel_ticket_id = models.IntegerField(
        _("pretix hotel ticket id"), blank=True, null=True
    )
    pretix_hotel_room_type_question_id = models.IntegerField(
        _("pretix hotel room type question id"), blank=True, null=True
    )
    pretix_hotel_checkin_question_id = models.IntegerField(
        _("pretix hotel check-in question id"), blank=True, null=True
    )
    pretix_hotel_checkout_question_id = models.IntegerField(
        _("pretix hotel checkout question id"), blank=True, null=True
    )

    introduction = I18nTextField(_("introduction"), blank=False)

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

    def __str__(self):
        return f"{self.name} <{self.code}>"

    class Meta:
        verbose_name = _("Conference")
        verbose_name_plural = _("Conferences")

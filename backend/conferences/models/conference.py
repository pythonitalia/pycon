from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeFramedModel, TimeStampedModel
from timezone_field import TimeZoneField

from helpers.models import GeoLocalizedModel
from i18n.fields import I18nCharField, I18nTextField

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
    url_mailchimp = models.URLField(_("url_mailchimp"), blank=True)

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

    def __str__(self):
        return f"{self.name} <{self.code}>"

    class Meta:
        verbose_name = _("Conference")
        verbose_name_plural = _("Conferences")

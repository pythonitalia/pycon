from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeFramedModel, TimeStampedModel
from timezone_field import TimeZoneField

from .deadline import Deadline


class Conference(TimeFramedModel, TimeStampedModel):
    name = models.CharField(_("name"), max_length=100)
    code = models.CharField(_("code"), max_length=10, unique=True)
    timezone = TimeZoneField()

    topics = models.ManyToManyField("conferences.Topic", verbose_name=_("topics"))
    languages = models.ManyToManyField(
        "languages.Language", verbose_name=_("languages")
    )
    audience_levels = models.ManyToManyField(
        "conferences.AudienceLevel", verbose_name=_("audience levels")
    )
    submission_types = models.ManyToManyField(
        "submissions.SubmissionType", verbose_name=_("submission types")
    )

    @property
    def is_cfp_open(self):
        try:
            cfp_deadline = self.deadlines.get(type=Deadline.TYPES.cfp)

            now = timezone.now()
            return cfp_deadline.start <= now <= cfp_deadline.end
        except Deadline.DoesNotExist:
            return False

    def __str__(self):
        return f"{self.name} <{self.code}>"

    class Meta:
        verbose_name = _("Conference")
        verbose_name_plural = _("Conferences")

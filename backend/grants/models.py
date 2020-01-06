from django.db import models
from django.utils.translation import ugettext_lazy as _
from helpers.constants import GENDERS
from model_utils import Choices
from model_utils.models import TimeStampedModel

OCCUPATIONS = Choices(
    ("developer", _("Developer")),
    ("student", _("Student")),
    ("researcher", _("Researcher")),
    ("unemployed", _("Unemployed")),
    ("other", _("Other")),
)

GRANT_TYPES = Choices(
    ("diversity", _("Diversity")),
    ("unemployed", _("Unemployed")),
    ("speaker", _("Speaker")),
)

INTERESTED_IN_VOLUNTEERING = Choices(
    ("no", _("No")), ("yes", _("Yes")), ("absolutely", _("My soul is yours to take!"))
)


class Grant(TimeStampedModel):
    name = models.CharField(_("name"), max_length=300)
    full_name = models.CharField(_("full name"), max_length=300)
    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        verbose_name=_("conference"),
        related_name="grants",
    )
    email = models.EmailField(_("email address"))
    age = models.PositiveSmallIntegerField(_("age"))
    gender = models.CharField(_("gender"), choices=GENDERS, max_length=10)
    occupation = models.CharField(_("occupation"), choices=OCCUPATIONS, max_length=10)
    grant_type = models.CharField(_("grant type"), choices=GRANT_TYPES, max_length=10)
    python_usage = models.TextField(_("How do they use python"))
    been_to_other_events = models.TextField(_("Have they been to other events?"))
    interested_in_volunteering = models.CharField(
        _("interested in volunteering"),
        choices=INTERESTED_IN_VOLUNTEERING,
        max_length=10,
    )
    needs_funds_for_travel = models.BooleanField(_("Needs funds for travel"))
    why = models.TextField(_("Why are you asking for a grant?"))
    notes = models.TextField(_("Notes"))
    travelling_from = models.CharField(_("Travelling from"), max_length=200)

    class Meta:
        unique_together = ["email", "conference"]

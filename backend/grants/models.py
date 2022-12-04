from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel

from helpers.constants import GENDERS

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
    class AgeGroup(models.TextChoices):
        RANGE_LESS_THAN_10 = "range_less_than_10", _("10 years old or under")
        RANGE_11_18 = "range_11_18", _("11 - 18 years old")
        RANGE_19_24 = "range_19_24", _("19 - 24 years old")
        RANGE_25_34 = "range_25_34", _("25 - 34 years old")
        RANGE_35_44 = "range_35_44", _("35 - 44 years old")
        RANGE_45_54 = "range_45_54", _("45 - 54 years old")
        RANGE_55_64 = "range_55_64", _("55 - 64 years old")
        RANGE_MORE_THAN_65 = "range_more_than_65", _("65 years or older")

    name = models.CharField(_("name"), max_length=300)
    full_name = models.CharField(_("full name"), max_length=300)
    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        verbose_name=_("conference"),
        related_name="grants",
    )
    user_id = models.IntegerField(verbose_name=_("user"), null=True)
    email = models.EmailField(_("email address"))
    age_group = models.CharField(
        _("Age group"), max_length=20, choices=AgeGroup.choices, blank=True
    )
    age = models.PositiveSmallIntegerField(_("age"), null=True)  # TODO: remove
    gender = models.CharField(_("gender"), choices=GENDERS, max_length=10, blank=True)
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
    notes = models.TextField(_("Notes"), blank=True)
    travelling_from = models.CharField(_("Travelling from"), max_length=200)

    def __str__(self):
        return f"{self.full_name}"

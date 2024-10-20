from conferences.querysets import ConferenceQuerySetMixin
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from countries import countries
from helpers.constants import GENDERS
from users.models import User


class GrantQuerySet(ConferenceQuerySetMixin, models.QuerySet):
    def of_user(self, user):
        return self.filter(user=user)


class AidCategory(models.Model):
    class AidType(models.TextChoices):
        TRAVEL = "travel", _("Travel")
        TICKET = "ticket", _("Ticket")
        ACCOMMODATION = "accommodation", _("Accommodation")
        OTHER = "other", _("Other")

    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        related_name="aid_categories",
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    max_amount = models.DecimalField(
        max_digits=6, decimal_places=0, help_text=_("Maximum amount for this category")
    )
    category = models.CharField(max_length=20, choices=AidType.choices)
    included_by_default = models.BooleanField(
        default=False,
        help_text="Automatically include this category in grants by default",
    )

    objects = GrantQuerySet().as_manager()

    def __str__(self):
        return f"{self.name} ({self.conference.name})"


class CountryAidAmount(models.Model):
    conference = models.ForeignKey(
        "conferences.Conference", on_delete=models.CASCADE, related_name="travel_costs"
    )
    country = models.CharField(
        "Country",
        choices=[(country.code, country.name) for country in countries],
        null=True,
        blank=True,
    )
    max_amount = models.DecimalField(
        max_digits=6, decimal_places=0, help_text=_("Maximum amount for this category")
    )

    objects = GrantQuerySet().as_manager()

    def __str__(self):
        return f"{self.country} ({self.conference.name}) - {self.max_amount}€"


class Grant(TimeStampedModel):
    # TextChoices
    class Status(models.TextChoices):
        pending = "pending", _("Pending")
        rejected = "rejected", _("Rejected")
        approved = "approved", _("Approved")
        waiting_list = "waiting_list", _("Waiting List")
        waiting_list_maybe = "waiting_list_maybe", _("Waiting List, Maybe")
        waiting_for_confirmation = (
            "waiting_for_confirmation",
            _("Waiting for confirmation"),
        )
        refused = "refused", _("Refused")
        confirmed = "confirmed", _("Confirmed")
        did_not_attend = "did_not_attend", _("Did Not Attend")

    REVIEW_SESSION_STATUSES_OPTIONS = [
        Status.rejected.value,
        Status.approved.value,
        Status.waiting_list.value,
        Status.waiting_list_maybe.value,
    ]

    class AgeGroup(models.TextChoices):
        range_less_than_10 = "range_less_than_10", _("10 years old or under")
        range_11_18 = "range_11_18", _("11 - 18 years old")
        range_19_24 = "range_19_24", _("19 - 24 years old")
        range_25_34 = "range_25_34", _("25 - 34 years old")
        range_35_44 = "range_35_44", _("35 - 44 years old")
        range_45_54 = "range_45_54", _("45 - 54 years old")
        range_55_64 = "range_55_64", _("55 - 64 years old")
        range_more_than_65 = "range_more_than_65", _("65 years or older")

    class Occupation(models.TextChoices):
        developer = "developer", _("Developer")
        student = "student", _("Student")
        researcher = "researcher", _("Researcher")
        unemployed = "unemployed", _("Unemployed")
        other = "other", _("Other")

    class GrantType(models.TextChoices):
        diversity = "diversity", _("Diversity")
        unemployed = "unemployed", _("Unemployed")
        speaker = "speaker", _("Speaker")

    class InterestedInVolunteering(models.TextChoices):
        no = "no", _("No")
        yes = "yes", _("Yes")
        absolutely = "absolutely", _("My soul is yours to take!")

    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        verbose_name=_("conference"),
        related_name="grants",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("user"),
        related_name="+",
    )
    email = models.EmailField(_("email address"))  # OLD FIELD

    # About You Section
    full_name = models.CharField(_("full name"), max_length=300)
    name = models.CharField(_("name"), max_length=300)
    age_group = models.CharField(
        _("Age group"), max_length=20, choices=AgeGroup.choices, blank=True
    )
    occupation = models.CharField(
        _("occupation"), choices=Occupation.choices, max_length=10
    )

    # Your Grant Section
    grant_type = models.CharField(
        _("grant type"), choices=GrantType.choices, max_length=10
    )
    travelling_from = models.CharField(
        _("Travelling from"),
        max_length=100,
        blank=True,
        null=True,
        choices=[(country.code, country.name) for country in countries],
    )
    needs_funds_for_travel = models.BooleanField(_("Needs funds for travel"))
    need_visa = models.BooleanField(_("Need visa/invitation letter?"), default=False)
    need_accommodation = models.BooleanField(_("Need accommodation"), default=False)

    why = models.TextField(_("Why are you asking for a grant?"))
    interested_in_volunteering = models.CharField(
        _("interested in volunteering"),
        choices=InterestedInVolunteering.choices,
        max_length=10,
    )

    # You and Python Section
    python_usage = models.TextField(_("How do they use python"))
    been_to_other_events = models.TextField(_("Have they been to other events?"))
    community_contribution = models.TextField(_("Community contribution"), blank=True)

    # Optional Information Section
    gender = models.CharField(_("gender"), choices=GENDERS, max_length=10, blank=True)
    notes = models.TextField(_("Notes"), blank=True)
    website = models.URLField(_("Website"), max_length=2048, blank=True)
    twitter_handle = models.CharField(_("Twitter handle"), max_length=15, blank=True)
    github_handle = models.CharField(_("GitHub handle"), blank=True, max_length=39)
    linkedin_url = models.URLField(_("LinkedIn url"), max_length=2048, blank=True)
    mastodon_handle = models.CharField(
        _("Mastodon handle"), max_length=2048, blank=True
    )

    # Grant Management and Processing
    status = models.CharField(
        _("status"), choices=Status.choices, max_length=30, default=Status.pending
    )

    # Financial amounts
    aid_categories = models.ManyToManyField(AidCategory, through="GrantAllocation")

    # Applicant Communication Tracking
    applicant_reply_sent_at = models.DateTimeField(
        _("applicant reply sent at"), null=True, blank=True
    )
    applicant_reply_deadline = models.DateTimeField(
        _("applicant reply deadline"), null=True, blank=True
    )

    # Voucher Management
    voucher_code = models.TextField(
        help_text=_("Voucher code generated for this grant."),
        blank=True,
        null=True,
    )
    pretix_voucher_id = models.IntegerField(
        help_text=_("ID of the voucher in the Pretix database"),
        blank=True,
        null=True,
    )
    voucher_email_sent_at = models.DateTimeField(
        help_text=_("When the email was last sent"), blank=True, null=True
    )
    internal_notes = models.TextField(
        _("Internal Notes"),
        help_text=_("Internal notes only available to the Financial Aid Commettie"),
        blank=True,
    )

    objects = GrantQuerySet().as_manager()

    def __str__(self):
        return f"{self.full_name}"

    def can_edit(self, user: User):
        return self.user_id == user.id

    def get_admin_url(self):
        return reverse(
            "admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name),
            args=(self.pk,),
        )

    def has_approved_travel(self):
        return self.aid_categories.filter(category=AidCategory.AidType.TRAVEL).exists()

    def has_approved_accommodation(self):
        return self.aid_categories.filter(
            category=AidCategory.AidType.ACCOMMODATION
        ).exists()


class GrantAllocation(models.Model):
    grant = models.ForeignKey(
        Grant, on_delete=models.CASCADE, related_name="allocations"
    )
    category = models.ForeignKey(AidCategory, on_delete=models.CASCADE)
    allocated_amount = models.DecimalField(
        max_digits=6,
        decimal_places=0,
        help_text="Actual amount allocated for this category",
    )

    def __str__(self):
        return (
            f"{self.grant.full_name} - {self.category.name} - {self.allocated_amount}€"
        )

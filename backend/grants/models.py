from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from countries import countries
from helpers.constants import GENDERS
from users.models import User


class Grant(TimeStampedModel):
    # TextChoices
    class Status(models.TextChoices):
        pending = "pending", _("Pending")
        rejected = "rejected", _("Rejected")
        approved = "approved", _("Approved")
        waiting_list = "waiting_list", _("Waiting List")
        waiting_list_maybe = "waiting_list_maybe", _("Waiting List, Maybe")
        waiting_for_confirmation = "waiting_for_confirmation", _(
            "Waiting for confirmation"
        )
        refused = "refused", _("Refused")
        confirmed = "confirmed", _("Confirmed")

    REVIEW_SESSION_STATUSES_OPTIONS = [
        Status.rejected.value,
        Status.approved.value,
        Status.waiting_list.value,
        Status.waiting_list_maybe.value,
    ]

    class CountryType(models.TextChoices):
        italy = "italy", _("Italy")
        europe = "europe", _("Europe")
        extra_eu = "extra_eu", _("Extra EU")

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

    class ApprovedType(models.TextChoices):
        ticket_only = "ticket_only", _("Ticket Only")
        ticket_travel = "ticket_travel", _("Ticket + Travel")
        ticket_accommodation = "ticket_accommodation", _("Ticket + Accommodation")
        ticket_travel_accommodation = "Ticket", _("Ticket + Travel + Accommodation")

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
    approved_type = models.CharField(
        verbose_name=_("approved type"),
        choices=ApprovedType.choices,
        max_length=30,
        blank=True,
        null=True,
    )

    # Financial amounts
    ticket_amount = models.DecimalField(
        verbose_name=_("ticket amount"),
        null=True,
        max_digits=6,
        decimal_places=2,
        default=0,
    )
    accommodation_amount = models.DecimalField(
        verbose_name=_("accommodation amount"),
        null=True,
        max_digits=6,
        decimal_places=2,
        default=0,
    )
    travel_amount = models.DecimalField(
        verbose_name=_("travel amount"),
        null=True,
        max_digits=6,
        decimal_places=2,
        default=0,
    )
    total_amount = models.DecimalField(
        verbose_name=_("total amount"),
        null=True,
        max_digits=6,
        decimal_places=2,
        default=0,
    )

    country_type = models.CharField(
        _("Country type"),
        max_length=10,
        choices=CountryType.choices,
        null=True,
        blank=True,
    )

    # Applicant Communication Tracking
    applicant_reply_sent_at = models.DateTimeField(
        _("applicant reply sent at"), null=True, blank=True
    )
    applicant_reply_deadline = models.DateTimeField(
        _("applicant reply deadline"), null=True, blank=True
    )
    applicant_message = models.TextField(_("applicant message"), null=True, blank=True)
    plain_thread_id = models.CharField(
        _("Plain threadID"),
        max_length=50,
        null=True,
        blank=True,
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_status = self.status
        self._original_approved_type = self.approved_type
        self._original_country_type = self.country_type

    def __str__(self):
        return f"{self.full_name}"

    def save(self, *args, **kwargs):
        self._update_country_type()
        self._calculate_grant_amounts()

        update_fields = kwargs.get("update_fields", None)
        if update_fields:
            update_fields.append("total_amount")
            update_fields.append("ticket_amount")
            update_fields.append("accommodation_amount")
            update_fields.append("travel_amount")
            update_fields.append("country_type")

        super().save(*args, **kwargs)

        self._original_approved_type = self.approved_type
        self._original_country_type = self.country_type
        self._original_status = self.status

    def _calculate_grant_amounts(self):
        if self.status != Grant.Status.approved:
            return

        if (
            self._original_status == self.status
            and self._original_approved_type == self.approved_type
            and self._original_country_type == self.country_type
        ):
            return

        conference = self.conference
        self.ticket_amount = conference.grants_default_ticket_amount or 0
        self.accommodation_amount = 0
        self.travel_amount = 0

        default_accommodation_amount = (
            conference.grants_default_accommodation_amount or 0
        )
        default_travel_from_italy_amount = (
            conference.grants_default_travel_from_italy_amount or 0
        )
        default_travel_from_europe_amount = (
            conference.grants_default_travel_from_europe_amount or 0
        )
        default_travel_from_extra_eu_amount = (
            conference.grants_default_travel_from_extra_eu_amount or 0
        )

        if self.approved_type in (
            Grant.ApprovedType.ticket_accommodation,
            Grant.ApprovedType.ticket_travel_accommodation,
        ):
            self.accommodation_amount = default_accommodation_amount

        if self.approved_type in (
            Grant.ApprovedType.ticket_travel_accommodation,
            Grant.ApprovedType.ticket_travel,
        ):
            if self.country_type == Grant.CountryType.italy:
                self.travel_amount = default_travel_from_italy_amount
            elif self.country_type == Grant.CountryType.europe:
                self.travel_amount = default_travel_from_europe_amount
            elif self.country_type == Grant.CountryType.extra_eu:
                self.travel_amount = default_travel_from_extra_eu_amount

        self.total_amount = (
            self.ticket_amount + self.accommodation_amount + self.travel_amount
        )

    def _update_country_type(self):
        if not self.travelling_from:
            return

        country = countries.get(code=self.travelling_from)
        assert country
        if country.code == "IT":
            self.country_type = Grant.CountryType.italy
        elif country.continent == "EU":
            self.country_type = Grant.CountryType.europe
        else:
            self.country_type = Grant.CountryType.extra_eu

    def can_edit(self, user: User):
        return self.user_id == user.id

    def get_admin_url(self):
        return reverse(
            "admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name),
            args=(self.pk,),
        )

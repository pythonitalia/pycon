from decimal import Decimal

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from conferences.querysets import ConferenceQuerySetMixin
from countries import countries
from helpers.constants import GENDERS
from users.models import User


class GrantQuerySet(ConferenceQuerySetMixin, models.QuerySet):
    def of_user(self, user):
        return self.filter(user=user)


class GrantReimbursementCategory(models.Model):
    """
    Define types of reimbursements available for a grant (e.g., Travel, Ticket, Accommodation).
    """

    class Category(models.TextChoices):
        TRAVEL = "travel", _("Travel")
        TICKET = "ticket", _("Ticket")
        ACCOMMODATION = "accommodation", _("Accommodation")
        OTHER = "other", _("Other")

    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        related_name="reimbursement_categories",
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    max_amount = models.DecimalField(
        max_digits=6,
        decimal_places=0,
        default=Decimal("0.00"),
        help_text=_("Maximum amount for this category"),
    )
    category = models.CharField(max_length=20, choices=Category.choices)
    included_by_default = models.BooleanField(
        default=False,
        help_text="Automatically include this category in grants by default",
    )

    objects = GrantQuerySet().as_manager()

    def __str__(self):
        return f"{self.name} ({self.conference.name})"

    class Meta:
        verbose_name = _("Grant Reimbursement Category")
        verbose_name_plural = _("Grant Reimbursement Categories")
        unique_together = [("conference", "category")]
        ordering = ["conference", "category"]


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

    class CountryType(models.TextChoices):
        italy = "italy", _("Italy")
        europe = "europe", _("Europe")
        extra_eu = "extra_eu", _("Extra EU")

    class AgeGroup(models.TextChoices):
        range_under_18 = "range_under_18", _("Under 18 years old")
        range_18_24 = "range_18_24", _("18 - 24 years old")
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
    grant_type = models.JSONField(_("grant type"), default=list)
    departure_country = models.CharField(
        _("Departure Country"),
        max_length=100,
        blank=True,
        null=True,
        choices=[(country.code, country.name) for country in countries],
    )
    nationality = models.CharField(
        _("Nationality"),
        max_length=100,
        blank=True,
        null=True,
    )
    departure_city = models.CharField(
        _("Departure city"),
        max_length=100,
        blank=True,
        null=True,
    )
    needs_funds_for_travel = models.BooleanField(_("Needs funds for travel"))
    need_visa = models.BooleanField(_("Need visa/invitation letter?"), default=False)
    need_accommodation = models.BooleanField(_("Need accommodation"), default=False)

    why = models.TextField(_("Why are you asking for a grant?"))

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
    pending_status = models.CharField(
        _("pending status"),
        choices=Status.choices,
        max_length=30,
        null=True,
        blank=True,
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

    # Voucher Management
    internal_notes = models.TextField(
        _("Internal Notes"),
        help_text=_("Internal notes only available to the Financial Aid Commettie"),
        blank=True,
    )

    reimbursement_categories = models.ManyToManyField(
        GrantReimbursementCategory, through="GrantReimbursement", related_name="grants"
    )

    objects = GrantQuerySet().as_manager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_status = self.status
        self._original_pending_status = self.pending_status
        self._original_country_type = self.country_type

    def __str__(self):
        return f"{self.full_name}"

    def save(self, *args, **kwargs):
        self._update_country_type()

        update_fields = kwargs.get("update_fields", None)
        if update_fields:
            update_fields.append("country_type")
            update_fields.append("pending_status")

        super().save(*args, **kwargs)

        self._original_country_type = self.country_type
        self._original_pending_status = self.pending_status
        self._original_status = self.status

    def _update_country_type(self):
        if not self.departure_country:
            return

        country = countries.get(code=self.departure_country)
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

    def has_approved_travel(self):
        return self.reimbursements.filter(
            category__category=GrantReimbursementCategory.Category.TRAVEL
        ).exists()

    def has_approved_accommodation(self):
        return self.reimbursements.filter(
            category__category=GrantReimbursementCategory.Category.ACCOMMODATION
        ).exists()

    @property
    def total_allocated_amount(self):
        return sum(r.granted_amount for r in self.reimbursements.all())

    def has_approved(self, type_):
        return self.reimbursements.filter(category__category=type_).exists()

    @property
    def current_or_pending_status(self):
        return self.pending_status or self.status


class GrantReimbursement(models.Model):
    """Links a Grant to its reimbursement categories and stores the actual amount granted."""

    grant = models.ForeignKey(
        Grant,
        on_delete=models.CASCADE,
        related_name="reimbursements",
        verbose_name=_("grant"),
    )
    category = models.ForeignKey(
        GrantReimbursementCategory,
        on_delete=models.CASCADE,
        verbose_name=_("reimbursement category"),
    )
    granted_amount = models.DecimalField(
        _("granted amount"),
        max_digits=6,
        decimal_places=0,
        help_text=_("Actual amount granted for this category"),
    )

    def __str__(self):
        return f"{self.grant.full_name} - {self.category.name} - {self.granted_amount}"

    class Meta:
        verbose_name = _("Grant Reimbursement")
        verbose_name_plural = _("Grant Reimbursements")
        unique_together = [("grant", "category")]
        ordering = ["grant", "category"]
        indexes = [
            models.Index(fields=["grant", "category"]),
        ]


class GrantConfirmPendingStatusProxy(Grant):
    class Meta:
        proxy = True
        verbose_name = _("Grant Confirm Pending Status")
        verbose_name_plural = _("Grants Confirm Pending Status")

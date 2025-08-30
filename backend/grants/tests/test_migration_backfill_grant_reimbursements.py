import pytest
from decimal import Decimal
from grants.models import GrantReimbursement, GrantReimbursementCategory
from grants.tests.factories import GrantFactory, GrantReimbursementCategoryFactory
from conferences.tests.factories import ConferenceFactory

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def conference_with_categories():
    """Create a conference with standard reimbursement categories."""
    conference = ConferenceFactory()

    GrantReimbursementCategoryFactory(
        conference=conference,
        category="ticket",
        name="Ticket",
        description="Conference ticket",
        max_amount=Decimal("100.00"),
        included_by_default=True,
    )

    GrantReimbursementCategoryFactory(
        conference=conference,
        category="travel",
        name="Travel",
        description="Travel support",
        max_amount=Decimal("500.00"),
        included_by_default=False,
    )

    GrantReimbursementCategoryFactory(
        conference=conference,
        category="accommodation",
        name="Accommodation",
        description="Accommodation support",
        max_amount=Decimal("200.00"),
        included_by_default=True,
    )

    return conference


def _create_reimbursements_for_grant(grant):
    """Simulate the migration logic for creating reimbursements from grant amounts."""
    categories = {
        c.category: c
        for c in GrantReimbursementCategory.objects.filter(conference=grant.conference)
    }

    if "ticket" in categories and grant.ticket_amount:
        GrantReimbursement.objects.get_or_create(
            grant=grant,
            category=categories["ticket"],
            defaults={"granted_amount": grant.ticket_amount},
        )

    if (
        grant.approved_type in ("ticket_travel", "ticket_travel_accommodation")
        and "travel" in categories
        and grant.travel_amount
    ):
        GrantReimbursement.objects.get_or_create(
            grant=grant,
            category=categories["travel"],
            defaults={"granted_amount": grant.travel_amount},
        )

    if (
        grant.approved_type in ("ticket_accommodation", "ticket_travel_accommodation")
        and "accommodation" in categories
        and grant.accommodation_amount
    ):
        GrantReimbursement.objects.get_or_create(
            grant=grant,
            category=categories["accommodation"],
            defaults={"granted_amount": grant.accommodation_amount},
        )


def _ensure_categories_exist_for_conference(conference):
    """Create grant reimbursement categories if they don't exist."""
    GrantReimbursementCategory.objects.get_or_create(
        conference=conference,
        category="ticket",
        defaults={
            "name": "Ticket",
            "description": "Conference ticket",
            "max_amount":  Decimal("150.00"),
            "included_by_default": True,
        },
    )
    GrantReimbursementCategory.objects.get_or_create(
        conference=conference,
        category="travel",
        defaults={
            "name": "Travel",
            "description": "Travel support",
            "max_amount":  Decimal("400.00"),
            "included_by_default": False,
        },
    )
    GrantReimbursementCategory.objects.get_or_create(
        conference=conference,
        category="accommodation",
        defaults={
            "name": "Accommodation",
            "description": "Accommodation support",
            "max_amount":  Decimal("300.00"),
            "included_by_default": True,
        },
    )


def test_creates_ticket_reimbursement_for_ticket_only_grant(conference_with_categories):
    grant = GrantFactory(
        conference=conference_with_categories,
        approved_type="ticket_only",
        ticket_amount=Decimal("100.00"),
        travel_amount=Decimal("0.00"),
        accommodation_amount=Decimal("0.00"),
    )

    _create_reimbursements_for_grant(grant)

    reimbursements = GrantReimbursement.objects.filter(grant=grant)
    assert reimbursements.count() == 1

    ticket_reimbursement = reimbursements.get(category__category="ticket")
    assert ticket_reimbursement.granted_amount == Decimal("100.00")


def test_creates_ticket_and_travel_reimbursement_for_ticket_travel_grant(
    conference_with_categories,
):
    grant = GrantFactory(
        conference=conference_with_categories,
        approved_type="ticket_travel",
        ticket_amount=Decimal("100.00"),
        travel_amount=Decimal("400.00"),
        accommodation_amount=Decimal("0.00"),
    )

    _create_reimbursements_for_grant(grant)

    reimbursements = GrantReimbursement.objects.filter(grant=grant)
    assert reimbursements.count() == 2

    ticket_reimbursement = reimbursements.get(category__category="ticket")
    travel_reimbursement = reimbursements.get(category__category="travel")

    assert ticket_reimbursement.granted_amount == Decimal("100.00")
    assert travel_reimbursement.granted_amount == Decimal("400.00")


def test_creates_ticket_and_accommodation_reimbursement_for_ticket_accommodation_grant(
    conference_with_categories,
):
    grant = GrantFactory(
        conference=conference_with_categories,
        approved_type="ticket_accommodation",
        ticket_amount=Decimal("100.00"),
        travel_amount=Decimal("0.00"),
        accommodation_amount=Decimal("200.00"),
    )

    _create_reimbursements_for_grant(grant)

    reimbursements = GrantReimbursement.objects.filter(grant=grant)
    assert reimbursements.count() == 2

    ticket_reimbursement = reimbursements.get(category__category="ticket")
    accommodation_reimbursement = reimbursements.get(category__category="accommodation")

    assert ticket_reimbursement.granted_amount == Decimal("100.00")
    assert accommodation_reimbursement.granted_amount == Decimal("200.00")


def test_creates_all_reimbursements_for_full_grant(conference_with_categories):
    grant = GrantFactory(
        conference=conference_with_categories,
        approved_type="ticket_travel_accommodation",
        ticket_amount=Decimal("100.00"),
        travel_amount=Decimal("400.00"),
        accommodation_amount=Decimal("200.00"),
    )

    _create_reimbursements_for_grant(grant)

    reimbursements = GrantReimbursement.objects.filter(grant=grant)
    assert reimbursements.count() == 3

    ticket_reimbursement = reimbursements.get(category__category="ticket")
    travel_reimbursement = reimbursements.get(category__category="travel")
    accommodation_reimbursement = reimbursements.get(category__category="accommodation")

    assert ticket_reimbursement.granted_amount == Decimal("100.00")
    assert travel_reimbursement.granted_amount == Decimal("400.00")
    assert accommodation_reimbursement.granted_amount == Decimal("200.00")


def test_skips_grants_without_approved_type(conference_with_categories):
    grant = GrantFactory(
        conference=conference_with_categories,
        approved_type=None,
        ticket_amount=Decimal("0.00"),
        travel_amount=Decimal("0.00"),
        accommodation_amount=Decimal("0.00"),
    )

    if grant.approved_type is not None and grant.approved_type != "":
        _create_reimbursements_for_grant(grant)

    reimbursements = GrantReimbursement.objects.filter(grant=grant)
    assert reimbursements.count() == 0


def test_preserves_total_amounts_after_migration(conference_with_categories):
    grants = [
        GrantFactory(
            conference=conference_with_categories,
            approved_type="ticket_only",
            ticket_amount=Decimal("100.00"),
            travel_amount=Decimal("0.00"),
            accommodation_amount=Decimal("0.00"),
        ),
        GrantFactory(
            conference=conference_with_categories,
            approved_type="ticket_travel",
            ticket_amount=Decimal("100.00"),
            travel_amount=Decimal("400.00"),
            accommodation_amount=Decimal("0.00"),
        ),
        GrantFactory(
            conference=conference_with_categories,
            approved_type="ticket_travel_accommodation",
            ticket_amount=Decimal("100.00"),
            travel_amount=Decimal("400.00"),
            accommodation_amount=Decimal("200.00"),
        ),
    ]

    for grant in grants:
        _create_reimbursements_for_grant(grant)

        original_total = (
            grant.ticket_amount + grant.travel_amount + grant.accommodation_amount
        )
        reimbursements_total = sum(
            r.granted_amount for r in GrantReimbursement.objects.filter(grant=grant)
        )
        assert original_total == reimbursements_total


def test_does_not_create_duplicates_when_run_multiple_times(conference_with_categories):
    grant = GrantFactory(
        conference=conference_with_categories,
        approved_type="ticket_travel_accommodation",
        ticket_amount=Decimal("100.00"),
        travel_amount=Decimal("400.00"),
        accommodation_amount=Decimal("200.00"),
    )

    _create_reimbursements_for_grant(grant)
    initial_count = GrantReimbursement.objects.filter(grant=grant).count()
    assert initial_count == 3

    _create_reimbursements_for_grant(grant)
    final_count = GrantReimbursement.objects.filter(grant=grant).count()
    assert final_count == 3


def test_creates_categories_with_conference_defaults():
    conference = ConferenceFactory(
        grants_default_ticket_amount=Decimal("150.00"),
        grants_default_accommodation_amount=Decimal("250.00"),
        grants_default_travel_from_extra_eu_amount=Decimal("550.00"),
    )

    _ensure_categories_exist_for_conference(conference)

    categories = GrantReimbursementCategory.objects.filter(conference=conference)
    assert categories.count() == 3

    ticket_cat = categories.get(category="ticket")
    travel_cat = categories.get(category="travel")
    accommodation_cat = categories.get(category="accommodation")

    assert ticket_cat.name == "Ticket"
    assert ticket_cat.max_amount == Decimal("150.00")
    assert ticket_cat.included_by_default is True

    assert travel_cat.name == "Travel"
    assert travel_cat.max_amount == Decimal("550.00")
    assert travel_cat.included_by_default is False

    assert accommodation_cat.name == "Accommodation"
    assert accommodation_cat.max_amount == Decimal("250.00")
    assert accommodation_cat.included_by_default is True

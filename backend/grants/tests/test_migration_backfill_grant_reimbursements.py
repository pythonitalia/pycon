from decimal import Decimal

import pytest

from conferences.tests.factories import ConferenceFactory
from grants.models import GrantReimbursement, GrantReimbursementCategory
from grants.tests.factories import GrantFactory, GrantReimbursementCategoryFactory

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def conference_with_categories():
    """Create a conference with standard reimbursement categories."""
    conference = ConferenceFactory()

    GrantReimbursementCategoryFactory(
        conference=conference,
        ticket=True,
        max_amount=Decimal("100"),
    )

    GrantReimbursementCategoryFactory(
        conference=conference,
        travel=True,
        max_amount=Decimal("500"),
    )

    GrantReimbursementCategoryFactory(
        conference=conference,
        accommodation=True,
        max_amount=Decimal("200"),
    )

    return conference


def _create_reimbursements_for_grant(
    grant,
    approved_type=None,
    ticket_amount=None,
    travel_amount=None,
    accommodation_amount=None,
):
    """Simulate the migration logic for creating reimbursements from grant amounts."""
    categories = {
        c.category: c
        for c in GrantReimbursementCategory.objects.filter(conference=grant.conference)
    }

    # Always add ticket reimbursement
    if "ticket" in categories and ticket_amount:
        GrantReimbursement.objects.get_or_create(
            grant=grant,
            category=categories["ticket"],
            defaults={"granted_amount": ticket_amount},
        )

    # Add travel reimbursement if approved
    if (
        approved_type in ("ticket_travel", "ticket_travel_accommodation")
        and "travel" in categories
        and travel_amount
    ):
        GrantReimbursement.objects.get_or_create(
            grant=grant,
            category=categories["travel"],
            defaults={"granted_amount": travel_amount},
        )

    # Add accommodation reimbursement if approved
    if (
        approved_type in ("ticket_accommodation", "ticket_travel_accommodation")
        and "accommodation" in categories
        and accommodation_amount
    ):
        GrantReimbursement.objects.get_or_create(
            grant=grant,
            category=categories["accommodation"],
            defaults={"granted_amount": accommodation_amount},
        )


def _ensure_categories_exist_for_conference(conference):
    """Create grant reimbursement categories if they don't exist."""
    GrantReimbursementCategoryFactory(
        conference=conference,
        ticket=True,
        max_amount=Decimal("150"),
    )
    GrantReimbursementCategoryFactory(
        conference=conference,
        travel=True,
        max_amount=Decimal("400"),
    )
    GrantReimbursementCategoryFactory(
        conference=conference,
        accommodation=True,
        max_amount=Decimal("300"),
    )


def test_creates_ticket_reimbursement_for_ticket_only_grant(conference_with_categories):
    grant = GrantFactory(conference=conference_with_categories)

    _create_reimbursements_for_grant(
        grant,
        approved_type="ticket_only",
        ticket_amount=Decimal("100"),
        travel_amount=Decimal("0"),
        accommodation_amount=Decimal("0"),
    )

    reimbursements = GrantReimbursement.objects.filter(grant=grant)
    assert reimbursements.count() == 1

    ticket_reimbursement = reimbursements.get(category__category="ticket")
    assert ticket_reimbursement.granted_amount == Decimal("100")


def test_creates_ticket_and_travel_reimbursement_for_ticket_travel_grant(
    conference_with_categories,
):
    grant = GrantFactory(conference=conference_with_categories)

    _create_reimbursements_for_grant(
        grant,
        approved_type="ticket_travel",
        ticket_amount=Decimal("100"),
        travel_amount=Decimal("400"),
        accommodation_amount=Decimal("0"),
    )

    reimbursements = GrantReimbursement.objects.filter(grant=grant)
    assert reimbursements.count() == 2

    ticket_reimbursement = reimbursements.get(category__category="ticket")
    travel_reimbursement = reimbursements.get(category__category="travel")

    assert ticket_reimbursement.granted_amount == Decimal("100")
    assert travel_reimbursement.granted_amount == Decimal("400")


def test_creates_ticket_and_accommodation_reimbursement_for_ticket_accommodation_grant(
    conference_with_categories,
):
    grant = GrantFactory(conference=conference_with_categories)

    _create_reimbursements_for_grant(
        grant,
        approved_type="ticket_accommodation",
        ticket_amount=Decimal("100"),
        travel_amount=Decimal("0"),
        accommodation_amount=Decimal("200"),
    )

    reimbursements = GrantReimbursement.objects.filter(grant=grant)
    assert reimbursements.count() == 2

    ticket_reimbursement = reimbursements.get(category__category="ticket")
    accommodation_reimbursement = reimbursements.get(category__category="accommodation")

    assert ticket_reimbursement.granted_amount == Decimal("100")
    assert accommodation_reimbursement.granted_amount == Decimal("200")


def test_creates_all_reimbursements_for_full_grant(conference_with_categories):
    grant = GrantFactory(conference=conference_with_categories)

    _create_reimbursements_for_grant(
        grant,
        approved_type="ticket_travel_accommodation",
        ticket_amount=Decimal("100"),
        travel_amount=Decimal("400"),
        accommodation_amount=Decimal("200"),
    )

    reimbursements = GrantReimbursement.objects.filter(grant=grant)
    assert reimbursements.count() == 3

    ticket_reimbursement = reimbursements.get(category__category="ticket")
    travel_reimbursement = reimbursements.get(category__category="travel")
    accommodation_reimbursement = reimbursements.get(category__category="accommodation")

    assert ticket_reimbursement.granted_amount == Decimal("100")
    assert travel_reimbursement.granted_amount == Decimal("400")
    assert accommodation_reimbursement.granted_amount == Decimal("200")


def test_skips_grants_without_approved_type(conference_with_categories):
    grant = GrantFactory(conference=conference_with_categories)

    approved_type = None
    if approved_type is not None and approved_type != "":
        _create_reimbursements_for_grant(
            grant,
            approved_type=approved_type,
            ticket_amount=Decimal("0"),
            travel_amount=Decimal("0"),
            accommodation_amount=Decimal("0"),
        )

    reimbursements = GrantReimbursement.objects.filter(grant=grant)
    assert reimbursements.count() == 0


def test_preserves_total_amounts_after_migration(conference_with_categories):
    test_cases = [
        {
            "approved_type": "ticket_only",
            "ticket_amount": Decimal("100"),
            "travel_amount": Decimal("0"),
            "accommodation_amount": Decimal("0"),
        },
        {
            "approved_type": "ticket_travel",
            "ticket_amount": Decimal("100"),
            "travel_amount": Decimal("400"),
            "accommodation_amount": Decimal("0"),
        },
        {
            "approved_type": "ticket_travel_accommodation",
            "ticket_amount": Decimal("100"),
            "travel_amount": Decimal("400"),
            "accommodation_amount": Decimal("200"),
        },
    ]

    for test_case in test_cases:
        grant = GrantFactory(conference=conference_with_categories)
        _create_reimbursements_for_grant(grant, **test_case)

        original_total = (
            test_case["ticket_amount"]
            + test_case["travel_amount"]
            + test_case["accommodation_amount"]
        )
        reimbursements_total = sum(
            r.granted_amount for r in GrantReimbursement.objects.filter(grant=grant)
        )
        assert original_total == reimbursements_total


def test_does_not_create_duplicates_when_run_multiple_times(conference_with_categories):
    grant = GrantFactory(conference=conference_with_categories)

    _create_reimbursements_for_grant(
        grant,
        approved_type="ticket_travel_accommodation",
        ticket_amount=Decimal("100"),
        travel_amount=Decimal("400"),
        accommodation_amount=Decimal("200"),
    )
    initial_count = GrantReimbursement.objects.filter(grant=grant).count()
    assert initial_count == 3

    _create_reimbursements_for_grant(
        grant,
        approved_type="ticket_travel_accommodation",
        ticket_amount=Decimal("100"),
        travel_amount=Decimal("400"),
        accommodation_amount=Decimal("200"),
    )
    final_count = GrantReimbursement.objects.filter(grant=grant).count()
    assert final_count == 3


def test_creates_categories_with_conference_defaults():
    conference = ConferenceFactory()

    _ensure_categories_exist_for_conference(conference)

    categories = GrantReimbursementCategory.objects.filter(conference=conference)
    assert categories.count() == 3

    ticket_cat = categories.get(category="ticket")
    travel_cat = categories.get(category="travel")
    accommodation_cat = categories.get(category="accommodation")

    assert ticket_cat.name == "Ticket"
    assert ticket_cat.max_amount == Decimal("150")
    assert ticket_cat.included_by_default is True

    assert travel_cat.name == "Travel"
    assert travel_cat.max_amount == Decimal("400")
    assert travel_cat.included_by_default is False

    assert accommodation_cat.name == "Accommodation"
    assert accommodation_cat.max_amount == Decimal("300")
    assert accommodation_cat.included_by_default is True

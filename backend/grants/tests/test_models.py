from decimal import Decimal

import pytest

from grants.models import Grant, GrantReimbursement
from grants.tests.factories import (
    GrantFactory,
    GrantReimbursementCategoryFactory,
    GrantReimbursementFactory,
)

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "data",
    [
        {
            "categories": ["ticket", "travel"],
            "departure_country": "IT",
            "expected_ticket_amount": 100,
            "expected_accommodation_amount": 0,
            "expected_travel_amount": 300,
        },
        {
            "categories": ["ticket"],
            "departure_country": "IT",
            "expected_ticket_amount": 100,
            "expected_accommodation_amount": 0,
            "expected_travel_amount": 0,
        },
        {
            "categories": ["ticket", "accommodation"],
            "departure_country": "FR",
            "expected_ticket_amount": 100,
            "expected_accommodation_amount": 200,
            "expected_travel_amount": 0,
        },
        {
            "categories": ["ticket", "travel"],
            "departure_country": "FR",
            "expected_ticket_amount": 100,
            "expected_accommodation_amount": 0,
            "expected_travel_amount": 400,
        },
        {
            "categories": ["ticket", "travel", "accommodation"],
            "departure_country": "AU",
            "expected_ticket_amount": 100,
            "expected_accommodation_amount": 200,
            "expected_travel_amount": 500,
        },
    ],
)
def test_calculate_grant_amounts(data):
    categories = data["categories"]
    departure_country = data["departure_country"]
    expected_ticket_amount = data["expected_ticket_amount"]
    expected_accommodation_amount = data["expected_accommodation_amount"]
    expected_travel_amount = data["expected_travel_amount"]

    grant = GrantFactory(
        pending_status=Grant.Status.approved,
        departure_country=departure_country,
    )

    # Create categories and reimbursements based on test data
    ticket_category = None
    travel_category = None
    accommodation_category = None

    if "ticket" in categories:
        ticket_category = GrantReimbursementCategoryFactory(
            conference=grant.conference,
            ticket=True,
            max_amount=Decimal("100"),
        )
        GrantReimbursementFactory(
            grant=grant,
            category=ticket_category,
            granted_amount=Decimal(expected_ticket_amount),
        )
    if "travel" in categories:
        travel_category = GrantReimbursementCategoryFactory(
            conference=grant.conference,
            travel=True,
            max_amount=Decimal("500"),
        )
        GrantReimbursementFactory(
            grant=grant,
            category=travel_category,
            granted_amount=Decimal(expected_travel_amount),
        )
    if "accommodation" in categories:
        accommodation_category = GrantReimbursementCategoryFactory(
            conference=grant.conference,
            accommodation=True,
            max_amount=Decimal("200"),
        )
        GrantReimbursementFactory(
            grant=grant,
            category=accommodation_category,
            granted_amount=Decimal(expected_accommodation_amount),
        )

    grant.refresh_from_db()

    # Verify individual reimbursement amounts
    if "ticket" in categories:
        ticket_reimbursement = GrantReimbursement.objects.get(
            grant=grant, category=ticket_category
        )
        assert ticket_reimbursement.granted_amount == Decimal(expected_ticket_amount)
    else:
        assert not GrantReimbursement.objects.filter(
            grant=grant, category__category="ticket"
        ).exists()

    if "travel" in categories:
        travel_reimbursement = GrantReimbursement.objects.get(
            grant=grant, category=travel_category
        )
        assert travel_reimbursement.granted_amount == Decimal(expected_travel_amount)
    else:
        assert not GrantReimbursement.objects.filter(
            grant=grant, category__category="travel"
        ).exists()

    if "accommodation" in categories:
        accommodation_reimbursement = GrantReimbursement.objects.get(
            grant=grant, category=accommodation_category
        )
        assert accommodation_reimbursement.granted_amount == Decimal(
            expected_accommodation_amount
        )
    else:
        assert not GrantReimbursement.objects.filter(
            grant=grant, category__category="accommodation"
        ).exists()

    # Verify total_allocated_amount sums correctly
    expected_total = (
        expected_ticket_amount + expected_accommodation_amount + expected_travel_amount
    )
    assert grant.total_allocated_amount == Decimal(expected_total)


def test_has_approved_ticket():
    grant = GrantFactory()
    assert not grant.has_approved_ticket()

    GrantReimbursementFactory(
        grant=grant,
        category__conference=grant.conference,
        category__ticket=True,
        granted_amount=Decimal("100"),
    )

    assert grant.has_approved_ticket()


def test_has_approved_travel():
    grant = GrantFactory()
    assert not grant.has_approved_travel()

    GrantReimbursementFactory(
        grant=grant,
        category__conference=grant.conference,
        category__travel=True,
        granted_amount=Decimal("500"),
    )

    assert grant.has_approved_travel()


def test_has_approved_accommodation():
    grant = GrantFactory()
    assert not grant.has_approved_accommodation()

    GrantReimbursementFactory(
        grant=grant,
        category__conference=grant.conference,
        category__accommodation=True,
        granted_amount=Decimal("200"),
    )

    assert grant.has_approved_accommodation()


def test_has_ticket_only_with_only_ticket():
    grant = GrantFactory()
    GrantReimbursementFactory(
        grant=grant,
        category__conference=grant.conference,
        category__ticket=True,
        granted_amount=Decimal("100"),
    )

    assert grant.has_ticket_only()


def test_has_ticket_only_with_ticket_and_travel():
    grant = GrantFactory()
    GrantReimbursementFactory(
        grant=grant,
        category__conference=grant.conference,
        category__ticket=True,
        granted_amount=Decimal("100"),
    )
    GrantReimbursementFactory(
        grant=grant,
        category__conference=grant.conference,
        category__travel=True,
        granted_amount=Decimal("500"),
    )

    assert not grant.has_ticket_only()


def test_has_ticket_only_without_ticket():
    grant = GrantFactory()
    GrantReimbursementFactory(
        grant=grant,
        category__conference=grant.conference,
        category__travel=True,
        granted_amount=Decimal("500"),
    )

    assert not grant.has_ticket_only()


def test_total_grantee_reimbursement_amount_excludes_ticket():
    grant = GrantFactory()
    GrantReimbursementFactory(
        grant=grant,
        category__conference=grant.conference,
        category__ticket=True,
        granted_amount=Decimal("100"),
    )
    GrantReimbursementFactory(
        grant=grant,
        category__conference=grant.conference,
        category__travel=True,
        granted_amount=Decimal("500"),
    )
    GrantReimbursementFactory(
        grant=grant,
        category__conference=grant.conference,
        category__accommodation=True,
        granted_amount=Decimal("200"),
    )

    # Should be 500 + 200 = 700, excluding ticket
    assert grant.total_grantee_reimbursement_amount == Decimal("700")


def test_total_grantee_reimbursement_amount_with_only_ticket():
    grant = GrantFactory()
    GrantReimbursementFactory(
        grant=grant,
        category__conference=grant.conference,
        category__ticket=True,
        granted_amount=Decimal("100"),
    )

    assert grant.total_grantee_reimbursement_amount == Decimal("0")


@pytest.mark.parametrize(
    "departure_country,country_type",
    [
        ("IT", Grant.CountryType.italy),
        ("FR", Grant.CountryType.europe),
        ("AU", Grant.CountryType.extra_eu),
        ("US", Grant.CountryType.extra_eu),
    ],
)
def test_sets_country_type(departure_country, country_type):
    grant = GrantFactory(departure_country=departure_country)

    assert grant.country_type == country_type


def test_sets_country_type_does_nothing_if_unset():
    grant = GrantFactory(departure_country=None)

    assert grant.country_type is None


def test_pending_status_no_longer_syncs_with_status():
    grant = GrantFactory(
        pending_status=Grant.Status.pending,
        status=Grant.Status.pending,
    )

    grant.status = Grant.Status.approved
    grant.save(update_fields=["status"])

    # Pending status should remain unchanged when status changes
    grant.refresh_from_db()

    assert grant.pending_status == Grant.Status.pending  # Should remain unchanged
    assert grant.status == Grant.Status.approved


def test_doesnt_sync_pending_status_if_different_values():
    grant = GrantFactory(
        pending_status=Grant.Status.refused,
        status=Grant.Status.pending,
    )

    grant.status = Grant.Status.waiting_for_confirmation
    grant.save()

    # Status should not be updated
    grant.refresh_from_db()

    assert grant.pending_status == Grant.Status.refused
    assert grant.status == Grant.Status.waiting_for_confirmation


@pytest.mark.skip(reason="We don't automatically create on save anymore")
def test_pending_status_none_means_no_pending_change():
    grant = GrantFactory(
        pending_status=None,
        status=Grant.Status.approved,
    )

    # When pending_status is None, the effective status should be the current status
    # This affects the _calculate_grant_amounts method
    grant.approved_type = Grant.ApprovedType.ticket_only
    grant.departure_country = "IT"
    grant.save()

    # Since effective status is approved (from status field), amounts should be calculated
    assert grant.ticket_amount is not None


@pytest.mark.skip(reason="We don't automatically create on save anymore")
def test_pending_status_set_overrides_current_status():
    grant = GrantFactory(
        pending_status=Grant.Status.approved,
        status=Grant.Status.pending,
    )

    # When pending_status is set, it should be used as the effective status
    grant.approved_type = Grant.ApprovedType.ticket_only
    grant.departure_country = "IT"
    grant.save()

    # Since effective status is approved (from pending_status), amounts should be calculated
    assert grant.ticket_amount is not None

from grants.models import Grant
from grants.tests.factories import GrantFactory
import pytest


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "data",
    [
        {
            "approved_type": Grant.ApprovedType.ticket_travel,
            "departure_country": "IT",
            "expected_ticket_amount": 100,
            "expected_accommodation_amount": 0,
            "expected_travel_amount": 300,
        },
        {
            "approved_type": Grant.ApprovedType.ticket_only,
            "departure_country": "IT",
            "expected_ticket_amount": 100,
            "expected_accommodation_amount": 0,
            "expected_travel_amount": 0,
        },
        {
            "approved_type": Grant.ApprovedType.ticket_accommodation,
            "departure_country": "FR",
            "expected_ticket_amount": 100,
            "expected_accommodation_amount": 200,
            "expected_travel_amount": 0,
        },
        {
            "approved_type": Grant.ApprovedType.ticket_travel,
            "departure_country": "FR",
            "expected_ticket_amount": 100,
            "expected_accommodation_amount": 0,
            "expected_travel_amount": 400,
        },
        {
            "approved_type": Grant.ApprovedType.ticket_travel_accommodation,
            "departure_country": "AU",
            "expected_ticket_amount": 100,
            "expected_accommodation_amount": 200,
            "expected_travel_amount": 500,
        },
    ],
)
def test_calculate_grant_amounts(data):
    approved_type = data["approved_type"]
    departure_country = data["departure_country"]
    expected_ticket_amount = data["expected_ticket_amount"]
    expected_accommodation_amount = data["expected_accommodation_amount"]
    expected_travel_amount = data["expected_travel_amount"]

    grant = GrantFactory(
        pending_status=Grant.Status.pending,
        approved_type=approved_type,
        departure_country=departure_country,
        conference__grants_default_ticket_amount=100,
        conference__grants_default_accommodation_amount=200,
        conference__grants_default_travel_from_italy_amount=300,
        conference__grants_default_travel_from_europe_amount=400,
        conference__grants_default_travel_from_extra_eu_amount=500,
    )

    grant.pending_status = Grant.Status.approved
    grant.save()

    grant.refresh_from_db()

    assert grant.ticket_amount == expected_ticket_amount
    assert grant.accommodation_amount == expected_accommodation_amount
    assert grant.travel_amount == expected_travel_amount
    assert (
        grant.total_amount
        == expected_ticket_amount
        + expected_accommodation_amount
        + expected_travel_amount
    )


def test_resets_amounts_on_approved_type_change():
    grant = GrantFactory(
        pending_status=Grant.Status.pending,
        approved_type=Grant.ApprovedType.ticket_only,
        departure_country="IT",
        conference__grants_default_ticket_amount=100,
        conference__grants_default_accommodation_amount=200,
        conference__grants_default_travel_from_italy_amount=300,
        conference__grants_default_travel_from_europe_amount=400,
        conference__grants_default_travel_from_extra_eu_amount=500,
    )

    grant.pending_status = Grant.Status.approved
    grant.save()

    assert grant.ticket_amount == 100
    assert grant.accommodation_amount == 0
    assert grant.travel_amount == 0
    assert grant.total_amount == 100

    grant.approved_type = Grant.ApprovedType.ticket_travel_accommodation
    grant.save()

    assert grant.ticket_amount == 100
    assert grant.accommodation_amount == 200
    assert grant.travel_amount == 300
    assert grant.total_amount == 600


def test_can_manually_change_amounts():
    grant = GrantFactory(
        pending_status=Grant.Status.pending,
        approved_type=Grant.ApprovedType.ticket_only,
        departure_country="IT",
        conference__grants_default_ticket_amount=100,
        conference__grants_default_accommodation_amount=200,
        conference__grants_default_travel_from_italy_amount=300,
        conference__grants_default_travel_from_europe_amount=400,
        conference__grants_default_travel_from_extra_eu_amount=500,
    )

    grant.pending_status = Grant.Status.approved
    grant.save(update_fields=["pending_status"])

    assert grant.ticket_amount == 100
    assert grant.accommodation_amount == 0
    assert grant.travel_amount == 0
    assert grant.total_amount == 100

    grant.ticket_amount = 20
    grant.accommodation_amount = 50
    grant.travel_amount = 0
    grant.total_amount = 70
    grant.save()

    assert grant.ticket_amount == 20
    assert grant.accommodation_amount == 50
    assert grant.travel_amount == 0
    assert grant.total_amount == 70


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

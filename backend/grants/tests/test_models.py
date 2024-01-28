from grants.models import Grant
from grants.tests.factories import GrantFactory
import pytest


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "data",
    [
        {
            "approved_type": Grant.ApprovedType.ticket_travel,
            "travelling_from": "IT",
            "expected_ticket_amount": 100,
            "expected_accommodation_amount": 0,
            "expected_travel_amount": 300,
        },
        {
            "approved_type": Grant.ApprovedType.ticket_only,
            "travelling_from": "IT",
            "expected_ticket_amount": 100,
            "expected_accommodation_amount": 400,
            "expected_travel_amount": 0,
        },
        {
            "approved_type": Grant.ApprovedType.ticket_accommodation,
            "travelling_from": "FR",
            "expected_ticket_amount": 100,
            "expected_accommodation_amount": 0,
            "expected_travel_amount": 0,
        },
        {
            "approved_type": Grant.ApprovedType.ticket_travel_accommodation,
            "travelling_from": "AU",
            "expected_ticket_amount": 100,
            "expected_accommodation_amount": 200,
            "expected_travel_amount": 500,
        },
    ],
)
def test_calculate_grant_amounts(data):
    approved_type = data["approved_type"]
    travelling_from = data["travelling_from"]
    expected_ticket_amount = data["expected_ticket_amount"]
    expected_accommodation_amount = data["expected_accommodation_amount"]
    expected_travel_amount = data["expected_travel_amount"]

    grant = GrantFactory(
        status=Grant.Status.pending,
        approved_type=approved_type,
        travelling_from=travelling_from,
        conference__grants_default_ticket_amount=100,
        conference__grants_default_accommodation_amount=200,
        conference__grants_default_travel_from_italy_amount=300,
        conference__grants_default_travel_from_europe_amount=400,
        conference__grants_default_travel_from_extra_eu_amount=500,
    )

    grant.status = Grant.Status.approved
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
        status=Grant.Status.pending,
        approved_type=Grant.ApprovedType.ticket_only,
        travelling_from="IT",
        conference__grants_default_ticket_amount=100,
        conference__grants_default_accommodation_amount=200,
        conference__grants_default_travel_from_italy_amount=300,
        conference__grants_default_travel_from_europe_amount=400,
        conference__grants_default_travel_from_extra_eu_amount=500,
    )

    grant.status = Grant.Status.approved
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
        status=Grant.Status.pending,
        approved_type=Grant.ApprovedType.ticket_only,
        travelling_from="IT",
        conference__grants_default_ticket_amount=100,
        conference__grants_default_accommodation_amount=200,
        conference__grants_default_travel_from_italy_amount=300,
        conference__grants_default_travel_from_europe_amount=400,
        conference__grants_default_travel_from_extra_eu_amount=500,
    )

    grant.status = Grant.Status.approved
    grant.save(update_fields=["status"])

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

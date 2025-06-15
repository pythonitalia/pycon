import pytest
from decimal import Decimal
from django.core.management import call_command
from grants.models import GrantReimbursement
from grants.tests.factories import GrantFactory


@pytest.mark.django_db
@pytest.mark.parametrize(
    "approved_type,expected_categories",
    [
        ("ticket_only", ["ticket"]),
        ("ticket_travel", ["ticket", "travel"]),
        ("ticket_accommodation", ["ticket", "accommodation"]),
        ("ticket_travel_accommodation", ["ticket", "travel", "accommodation"]),
    ],
)
def test_backfill_grant_reimbursements_all_types(approved_type, expected_categories):
    ticket_amount = Decimal("100.00")
    travel_amount = Decimal("150.00")
    accommodation_amount = Decimal("200.00")

    grant = GrantFactory(
        approved_type=approved_type,
        status="confirmed",
        ticket_amount=ticket_amount,
        travel_amount=travel_amount,
        accommodation_amount=accommodation_amount,
    )

    call_command("backfill_grant_reimbursements")

    reimbursements = GrantReimbursement.objects.filter(grant=grant)
    assert reimbursements.count() == len(expected_categories)

    for category in expected_categories:
        r = reimbursements.get(category__category=category)
        if category == "ticket":
            assert r.granted_amount == ticket_amount
        elif category == "travel":
            assert r.granted_amount == travel_amount
        elif category == "accommodation":
            assert r.granted_amount == accommodation_amount


def test_grant_reimbursement_does_not_duplicate_on_rerun():
    grant = GrantFactory(
        approved_type="ticket_travel_accommodation",
        status="approved",
        ticket_amount=Decimal("100.00"),
        travel_amount=Decimal("100.00"),
        accommodation_amount=Decimal("100.00"),
    )

    call_command("backfill_grant_reimbursements")
    initial_count = GrantReimbursement.objects.filter(grant=grant).count()
    assert initial_count == 3

    call_command("backfill_grant_reimbursements")
    second_count = GrantReimbursement.objects.filter(grant=grant).count()
    assert second_count == 3  # no duplicates


def test_total_amount_consistency():
    grant = GrantFactory(
        approved_type="ticket_travel",
        status="approved",
        ticket_amount=Decimal("120.00"),
        travel_amount=Decimal("80.00"),
        accommodation_amount=Decimal("0.00"),
    )

    call_command("backfill_grant_reimbursements")
    reimbursements = GrantReimbursement.objects.filter(grant=grant)
    total = sum(r.granted_amount for r in reimbursements)
    expected = grant.ticket_amount + grant.travel_amount
    assert total == expected

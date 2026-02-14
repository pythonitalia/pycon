import pytest
from .factories import (
    GrantFactory,
    GrantReimbursementCategoryFactory,
    GrantReimbursementFactory,
)
from grants.summary import GrantSummary
from conferences.tests.factories import ConferenceFactory


@pytest.fixture
def grants_set():
    conference = ConferenceFactory()

    GrantFactory.create_batch(
        5,
        conference=conference,
        status="approved",
        pending_status="approved",
        country_type="italy",
        gender="female",
        departure_country="IT",
    )
    GrantFactory.create_batch(
        3,
        conference=conference,
        status="rejected",
        pending_status="rejected",
        country_type="europe",
        gender="male",
        departure_country="FR",
    )
    GrantFactory.create_batch(
        7,
        conference=conference,
        status="waiting_list",
        pending_status="waiting_list",
        country_type="extra_eu",
        gender="other",
        departure_country="US",
    )

    return conference


def test_grant_summary_calculation_by_country(grants_set):
    conference = grants_set
    summary = GrantSummary().calculate(conference_id=conference.id)

    assert summary["country_stats"][("Europe", "Italy 🇮🇹", "IT")]["approved"] == 5
    assert summary["country_stats"][("Europe", "France 🇫🇷", "FR")]["rejected"] == 3
    assert (
        summary["country_stats"][("North America", "United States 🇺🇸", "US")][
            "waiting_list"
        ]
        == 7
    )
    assert summary["totals_per_continent"]["Europe"]["approved"] == 5
    assert summary["totals_per_continent"]["Europe"]["rejected"] == 3
    assert summary["totals_per_continent"]["North America"]["waiting_list"] == 7


def test_grant_summary_calculation_by_gender(grants_set):
    conference = grants_set
    summary = GrantSummary().calculate(conference_id=conference.id)

    assert summary["gender_stats"]["female"]["approved"] == 5
    assert summary["gender_stats"]["male"]["rejected"] == 3
    assert summary["gender_stats"]["other"]["waiting_list"] == 7


def test_grant_summary_calculation_by_status(grants_set):
    conference = grants_set
    summary = GrantSummary().calculate(conference_id=conference.id)

    assert summary["status_totals"]["approved"] == 5
    assert summary["status_totals"]["rejected"] == 3
    assert summary["status_totals"]["waiting_list"] == 7
    assert summary["total_grants"] == 15


@pytest.mark.django_db
def test_grant_summary_with_null_pending_status():
    conference = ConferenceFactory()

    GrantFactory.create_batch(
        3,
        conference=conference,
        status="approved",
        pending_status=None,
        departure_country="IT",
        gender="female",
    )
    GrantFactory.create_batch(
        2,
        conference=conference,
        status="rejected",
        pending_status=None,
        departure_country="FR",
        gender="male",
    )

    summary = GrantSummary().calculate(conference_id=conference.id)

    # status_totals should reflect the fallback status values
    assert summary["status_totals"]["approved"] == 3
    assert summary["status_totals"]["rejected"] == 2
    assert summary["total_grants"] == 5

    # country stats should also work
    assert summary["country_stats"][("Europe", "Italy 🇮🇹", "IT")]["approved"] == 3
    assert summary["country_stats"][("Europe", "France 🇫🇷", "FR")]["rejected"] == 2

    # gender stats should use the fallback too
    assert summary["gender_stats"]["female"]["approved"] == 3
    assert summary["gender_stats"]["male"]["rejected"] == 2


@pytest.mark.django_db
def test_grant_summary_with_mixed_pending_status():
    conference = ConferenceFactory()

    # Grant with pending_status set (pending_status takes precedence)
    GrantFactory.create_batch(
        2,
        conference=conference,
        status="pending",
        pending_status="approved",
        departure_country="IT",
    )
    # Grant with pending_status=None (falls back to status)
    GrantFactory.create_batch(
        3,
        conference=conference,
        status="rejected",
        pending_status=None,
        departure_country="IT",
    )

    summary = GrantSummary().calculate(conference_id=conference.id)

    assert summary["status_totals"]["approved"] == 2
    assert summary["status_totals"]["rejected"] == 3
    assert summary["total_grants"] == 5


@pytest.mark.django_db
def test_grant_summary_financial_data_with_null_pending_status():
    conference = ConferenceFactory()

    ticket_category = GrantReimbursementCategoryFactory(
        conference=conference,
        ticket=True,
    )

    grant_with_status = GrantFactory(
        conference=conference,
        status="approved",
        pending_status=None,
        departure_country="IT",
    )
    GrantReimbursementFactory(
        grant=grant_with_status,
        category=ticket_category,
        granted_amount=100,
    )

    grant_with_pending = GrantFactory(
        conference=conference,
        status="pending",
        pending_status="confirmed",
        departure_country="IT",
    )
    GrantReimbursementFactory(
        grant=grant_with_pending,
        category=ticket_category,
        granted_amount=200,
    )

    summary = GrantSummary().calculate(conference_id=conference.id)

    assert summary["financial_summary"]["approved"] == 100
    assert summary["financial_summary"]["confirmed"] == 200
    # approved + confirmed are both BUDGET_STATUSES
    assert summary["total_amount"] == 300

    # reimbursement category summary should also work
    assert summary["reimbursement_category_summary"]["ticket"]["approved"] == 1
    assert summary["reimbursement_category_summary"]["ticket"]["confirmed"] == 1

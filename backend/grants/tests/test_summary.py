import pytest
from .factories import GrantFactory
from grants.summary import GrantSummary
from conferences.tests.factories import ConferenceFactory


@pytest.fixture
def grants_set():
    conference = ConferenceFactory()

    GrantFactory.create_batch(
        5,
        conference=conference,
        status="approved",
        country_type="italy",
        gender="female",
        travelling_from="IT",
    )
    GrantFactory.create_batch(
        3,
        conference=conference,
        status="rejected",
        country_type="europe",
        gender="male",
        travelling_from="FR",
    )
    GrantFactory.create_batch(
        7,
        conference=conference,
        status="waiting_list",
        country_type="extra_eu",
        gender="other",
        travelling_from="US",
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

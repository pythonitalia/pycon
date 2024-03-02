from conferences.tests.factories import KeynoteFactory
from i18n.strings import LazyI18nString
import pytest
from submissions.models import Submission
from submissions.tests.factories import SubmissionFactory

pytestmark = pytest.mark.django_db


def _search_events_for_schedule(client, **input):
    return client.query(
        """query SearchEventsForSchedule($conferenceId: ID!, $query: String!) {
        searchEventsForSchedule(conferenceId: $conferenceId, query: $query) {
            results {
                __typename
                ... on Submission {
                    id
                }
                ... on Keynote {
                    id
                }
            }
        }
    }""",
        variables={**input},
    )


@pytest.mark.parametrize("user_to_test", ["admin_user", "user", "not_authenticated"])
def test_cannot_search_without_permission(
    admin_graphql_api_client,
    user_to_test,
    admin_user,
    user,
    conference_with_schedule_setup,
):
    if user_to_test == "admin_user":
        admin_graphql_api_client.force_login(admin_user)
    elif user_to_test == "user":
        admin_graphql_api_client.force_login(user)

    conference = conference_with_schedule_setup
    response = _search_events_for_schedule(
        admin_graphql_api_client, conferenceId=conference.id, query="TDD"
    )

    assert response["errors"][0]["message"] == "Cannot edit schedule"
    assert not response.get("data")


def test_search(
    admin_graphql_api_client, admin_superuser, conference_with_schedule_setup
):
    admin_graphql_api_client.force_login(admin_superuser)
    conference = conference_with_schedule_setup

    submission_1 = SubmissionFactory(
        conference=conference,
        status=Submission.STATUS.accepted,
        title=LazyI18nString({"en": "My TDD talk", "it": ""}),
        speaker__name="John Doe",
    )

    SubmissionFactory(
        conference=conference,
        status=Submission.STATUS.accepted,
        title=LazyI18nString({"en": "Unrelated submission", "it": ""}),
        speaker__name="Jane Doe",
    )

    keynote_1 = KeynoteFactory(
        conference=conference,
        title=LazyI18nString({"en": "A keynote about TDD, yes, really.", "it": ""}),
    )

    KeynoteFactory(
        conference=conference,
        title=LazyI18nString({"en": "Unrelated keynote.", "it": ""}),
    )

    SubmissionFactory(
        conference=conference,
        status=Submission.STATUS.rejected,
        title=LazyI18nString({"en": "TDD: How to do it", "it": ""}),
    )

    response = _search_events_for_schedule(
        admin_graphql_api_client, conferenceId=conference.id, query="TDD"
    )

    assert not response.get("errors")
    data = response["data"]

    assert len(data["searchEventsForSchedule"]["results"]) == 2
    assert {"__typename": "Submission", "id": str(submission_1.hashid)} in data[
        "searchEventsForSchedule"
    ]["results"]
    assert {"__typename": "Keynote", "id": str(keynote_1.id)} in data[
        "searchEventsForSchedule"
    ]["results"]

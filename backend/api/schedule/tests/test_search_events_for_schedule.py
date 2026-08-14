import pytest

from conferences.tests.factories import (
    ConferenceFactory,
    DurationFactory,
    KeynoteFactory,
    KeynoteSpeakerFactory,
)
from i18n.strings import LazyI18nString
from participants.tests.factories import ParticipantFactory
from submissions.models import Submission
from submissions.tests.factories import SubmissionFactory, SubmissionTypeFactory
from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


SEARCH_EVENTS_QUERY = """
query SearchEvents($conferenceId: ID!, $query: String!) {
  searchEvents: searchEventsForSchedule(
    conferenceId: $conferenceId
    query: $query
  ) {
    results {
      ... on Submission {
        id
        title(language: "en")
        italianTitle: title(language: "it")
        duration {
          id
          duration
        }
        type {
          id
          name
        }
        languages {
          id
          name
          code
        }
        speaker {
          id
          fullName
          participant {
            speakerAvailabilities
          }
        }
      }
      ... on Keynote {
        id
        title
        speakers {
          id
          fullName
        }
      }
    }
  }
}
"""


MULTI_CONFERENCE_SEARCH_EVENTS_QUERY = """
query SearchEvents($firstConferenceId: ID!, $secondConferenceId: ID!) {
  first: searchEventsForSchedule(
    conferenceId: $firstConferenceId
    query: "Shared"
  ) {
    results {
      ... on Submission {
        speaker {
          participant {
            speakerAvailabilities
          }
        }
      }
    }
  }
  second: searchEventsForSchedule(
    conferenceId: $secondConferenceId
    query: "Shared"
  ) {
    results {
      ... on Submission {
        speaker {
          participant {
            speakerAvailabilities
          }
        }
      }
    }
  }
}
"""


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


@pytest.mark.parametrize(
    ("event_count", "expected_queries"),
    [(1, 9), (4, 9)],
)
def test_frontend_search_events_query(
    admin_graphql_api_client,
    admin_superuser,
    conference_with_schedule_setup,
    django_assert_num_queries,
    event_count,
    expected_queries,
):
    conference = conference_with_schedule_setup
    duration = DurationFactory(
        conference=conference,
        duration=45,
        name="45 minutes",
    )
    submission_type = SubmissionTypeFactory(name="Talk")
    submissions = []
    keynotes = []

    for index in range(event_count):
        speaker = UserFactory(full_name=f"Proposal Speaker {index + 1}")
        ParticipantFactory(
            conference=conference,
            user=speaker,
            speaker_availabilities={"day": index + 1},
        )
        submission = SubmissionFactory(
            conference=conference,
            duration=duration,
            languages=["en"],
            speaker=speaker,
            status=Submission.STATUS.accepted,
            title=LazyI18nString(
                {
                    "en": f"GraphQL Talk {index + 1}",
                    "it": f"Talk GraphQL {index + 1}",
                }
            ),
            type=submission_type,
        )
        submissions.append(submission)

        keynote_speaker = UserFactory(full_name=f"Keynote Speaker {index + 1}")
        ParticipantFactory(
            conference=conference,
            user=keynote_speaker,
        )
        keynote = KeynoteFactory(
            conference=conference,
            title=LazyI18nString(
                {
                    "en": f"GraphQL Keynote {index + 1}",
                    "it": f"Keynote GraphQL {index + 1}",
                }
            ),
        )
        KeynoteSpeakerFactory(keynote=keynote, user=keynote_speaker)
        keynotes.append((keynote, keynote_speaker))

    language = submissions[0].languages.get()
    admin_graphql_api_client.force_login(admin_superuser)

    with django_assert_num_queries(expected_queries):
        response = admin_graphql_api_client.query(
            SEARCH_EVENTS_QUERY,
            variables={"conferenceId": str(conference.id), "query": "GraphQL"},
        )

    assert "errors" not in response
    expected_data = {
        "searchEvents": {
            "results": [
                *[
                    {
                        "id": submission.hashid,
                        "title": submission.title.localize("en"),
                        "italianTitle": submission.title.localize("it"),
                        "duration": {
                            "id": str(duration.id),
                            "duration": duration.duration,
                        },
                        "type": {
                            "id": str(submission_type.id),
                            "name": submission_type.name,
                        },
                        "languages": [
                            {
                                "id": str(language.id),
                                "name": language.name,
                                "code": language.code,
                            }
                        ],
                        "speaker": {
                            "id": str(submission.speaker_id),
                            "fullName": submission.speaker.full_name,
                            "participant": {
                                "speakerAvailabilities": {
                                    "day": index + 1,
                                }
                            },
                        },
                    }
                    for index, submission in enumerate(submissions)
                ],
                *[
                    {
                        "id": str(keynote.id),
                        "title": keynote.title.localize("en"),
                        "speakers": [
                            {
                                "id": str(speaker.id),
                                "fullName": speaker.full_name,
                            }
                        ],
                    }
                    for keynote, speaker in keynotes
                ],
            ]
        }
    }
    response["data"]["searchEvents"]["results"].sort(key=lambda result: result["id"])
    expected_data["searchEvents"]["results"].sort(key=lambda result: result["id"])
    assert response["data"] == expected_data


def test_frontend_search_events_query_keeps_participants_scoped_by_conference(
    admin_graphql_api_client,
    admin_superuser,
    django_assert_num_queries,
):
    conferences = [ConferenceFactory(), ConferenceFactory()]
    speaker = UserFactory(full_name="Shared Speaker")

    for index, conference in enumerate(conferences, start=1):
        ParticipantFactory(
            conference=conference,
            user=speaker,
            speaker_availabilities={"conference": index},
        )
        SubmissionFactory(
            conference=conference,
            speaker=speaker,
            status=Submission.STATUS.accepted,
            title=LazyI18nString({"en": f"Shared Talk {index}", "it": ""}),
        )

    admin_graphql_api_client.force_login(admin_superuser)
    with django_assert_num_queries(10):
        response = admin_graphql_api_client.query(
            MULTI_CONFERENCE_SEARCH_EVENTS_QUERY,
            variables={
                "firstConferenceId": str(conferences[0].id),
                "secondConferenceId": str(conferences[1].id),
            },
        )

    assert "errors" not in response
    assert response["data"] == {
        "first": {
            "results": [
                {
                    "speaker": {
                        "participant": {"speakerAvailabilities": {"conference": 1}}
                    }
                }
            ]
        },
        "second": {
            "results": [
                {
                    "speaker": {
                        "participant": {"speakerAvailabilities": {"conference": 2}}
                    }
                }
            ]
        },
    }


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

    submission_2 = SubmissionFactory(
        conference=conference,
        status=Submission.STATUS.proposed,
        pending_status=Submission.STATUS.accepted,
        title=LazyI18nString({"en": "TDD talk", "it": ""}),
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

    assert len(data["searchEventsForSchedule"]["results"]) == 3
    assert {"__typename": "Submission", "id": str(submission_1.hashid)} in data[
        "searchEventsForSchedule"
    ]["results"]
    assert {"__typename": "Keynote", "id": str(keynote_1.id)} in data[
        "searchEventsForSchedule"
    ]["results"]
    assert {"__typename": "Submission", "id": str(submission_2.hashid)} in data[
        "searchEventsForSchedule"
    ]["results"]

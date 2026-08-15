import pytest

from conferences.tests.factories import ConferenceFactory
from participants.tests.factories import ParticipantFactory
from submissions.models import Submission
from submissions.tests.factories import SubmissionFactory
from users.tests.factories import UserFactory


pytestmark = pytest.mark.django_db


SUBMISSION_ACCORDION_FRAGMENT = """
    fragment submissionAccordion on Submission {
      id
      title(language: $language)
      elevatorPitch(language: $language)
      type {
        name
      }
      tags {
        name
        id
      }
      audienceLevel {
        id
        name
      }
      duration {
        id
        name
        duration
      }
      languages {
        id
        name
        code
      }
      myVote {
        id
        value
      }
      speaker {
        id
        fullName
      }
    }
"""


VOTING_SUBMISSIONS_QUERY = (
    """
    query VotingSubmissions(
      $conference: String!
      $language: String!
      $languages: [String!]
      $voted: Boolean
      $tags: [String!]
      $types: [String!]
      $audienceLevels: [String!]
      $page: Int
    ) {
      submissions(
        code: $conference
        languages: $languages
        voted: $voted
        tags: $tags
        types: $types
        audienceLevels: $audienceLevels
        page: $page
        pageSize: 100
      ) {
        pageInfo {
          totalPages
          totalItems
        }
        items {
          ...submissionAccordion
        }
      }
    }
    """
    + SUBMISSION_ACCORDION_FRAGMENT
)


DYNAMIC_CONTENT_PROPOSALS_QUERY = (
    """
    query DynamicContentDisplaySectionProposals(
      $code: String!
      $language: String!
    ) {
      submissions(code: $code, onlyAccepted: true, pageSize: 300) {
        items {
          ...submissionAccordion
          id
          speaker {
            id
            fullName
            participant {
              id
              photo
              bio
            }
          }
        }
      }
    }
    """
    + SUBMISSION_ACCORDION_FRAGMENT
)


@pytest.mark.parametrize(
    ("submission_count", "expected_queries"),
    [(1, 16), (4, 19)],
)
def test_voting_submissions_frontend_query(
    graphql_client,
    django_assert_num_queries,
    mock_has_ticket,
    submission_count,
    expected_queries,
):
    user = UserFactory()
    graphql_client.force_login(user)
    conference = ConferenceFactory()
    submissions = SubmissionFactory.create_batch(
        submission_count,
        conference=conference,
        tags=["graphql"],
    )
    mock_has_ticket(conference)

    with django_assert_num_queries(expected_queries):
        response = graphql_client.query(
            VOTING_SUBMISSIONS_QUERY,
            variables={"conference": conference.code, "language": "en"},
        )

    assert "errors" not in response
    items = response["data"]["submissions"]["items"]
    assert len(items) == submission_count
    assert {item["id"] for item in items} == {
        submission.hashid for submission in submissions
    }


@pytest.mark.parametrize(
    ("submission_count", "expected_queries"),
    [(1, 12), (4, 21)],
)
def test_dynamic_content_proposals_frontend_query(
    graphql_client,
    django_assert_num_queries,
    submission_count,
    expected_queries,
):
    conference = ConferenceFactory()
    submissions = SubmissionFactory.create_batch(
        submission_count,
        conference=conference,
        status=Submission.STATUS.accepted,
        tags=["graphql"],
    )
    participants = [
        ParticipantFactory(
            conference=conference,
            user=submission.speaker,
            public_profile=True,
        )
        for submission in submissions
    ]

    with django_assert_num_queries(expected_queries):
        response = graphql_client.query(
            DYNAMIC_CONTENT_PROPOSALS_QUERY,
            variables={"code": conference.code, "language": "en"},
        )

    assert "errors" not in response
    items = response["data"]["submissions"]["items"]
    assert len(items) == submission_count
    assert {item["speaker"]["participant"]["id"] for item in items} == {
        participant.hashid for participant in participants
    }

import pytest

from conferences.tests.factories import ConferenceFactory
from grants.tests.factories import GrantFactory
from participants.tests.factories import ParticipantFactory
from reviews.tests.factories import AvailableScoreOptionFactory, UserReviewFactory
from submissions.tests.factories import SubmissionFactory
from users.tests.factories import UserFactory
from voting.tests.factories.ranking import RankSubmissionFactory

pytestmark = pytest.mark.django_db

QUERY = """query($sessionId: ID!, $proposalId: ID!) {
    reviewProposal(reviewSessionId: $sessionId, proposalId: $proposalId) {
        id
        title { en it }
        elevatorPitchHtml { en }
        tags { name }
        rankings { tag rank total }
        isMine
        speaker {
            fullName
            gender
            country
            bio
            grant { status }
            proposalsCount
            otherProposals { id }
        }
        votes { reviewerName isMine scoreLabel scoreValue comment }
        myVote { scoreOptionId comment }
    }
}"""


def _review_proposal(client, review_session, proposal):
    return client.query(
        QUERY, variables={"sessionId": review_session.id, "proposalId": proposal.id}
    )


@pytest.mark.parametrize(
    "gender,shown_gender", [("female", "Female"), ("not_say", None)]
)
def test_review_proposal(
    admin_graphql_api_client,
    make_reviewer,
    proposals_review_session,
    gender,
    shown_gender,
):
    review_session = proposals_review_session
    conference = review_session.conference
    reviewer = make_reviewer(conference)
    speaker = UserFactory(full_name="Ada Lovelace", gender=gender, country="IT")
    proposal = SubmissionFactory(
        conference=conference,
        speaker=speaker,
        languages=["en"],
        tags=["python"],
        elevator_pitch={
            "en": "**Fast**\n<script>alert(1)</script>\n\n- one\n- two\n\nEnd",
            "it": "",
        },
    )
    other_proposal = SubmissionFactory(conference=conference, speaker=speaker)
    SubmissionFactory(conference=conference, speaker=speaker, status="cancelled")
    ParticipantFactory(conference=conference, user=speaker, bio="Hi")
    GrantFactory(conference=conference, user=speaker, status="approved")
    RankSubmissionFactory(
        submission=proposal,
        tag=proposal.tags.get(),
        rank=3,
        total_submissions_per_tag=40,
    )
    yes = AvailableScoreOptionFactory(
        review_session=review_session, numeric_value=2, label="Yes"
    )
    UserReviewFactory(
        review_session=review_session,
        proposal=proposal,
        user=UserFactory(full_name="Other Reviewer"),
        score=None,
        comment="Not my area",
    )
    UserReviewFactory(
        review_session=review_session,
        proposal=proposal,
        user=reviewer,
        score=yes,
        comment="Mine",
    )
    admin_graphql_api_client.force_login(reviewer)

    data = _review_proposal(admin_graphql_api_client, review_session, proposal)["data"][
        "reviewProposal"
    ]

    assert data["title"] == {"en": proposal.title.localize("en"), "it": None}
    assert data["elevatorPitchHtml"] == {
        "en": "<strong>Fast</strong><br>alert(1)<ul><li>one</li><li>two</li></ul>End"
    }
    assert data["tags"] == [{"name": "python"}]
    assert data["rankings"] == [{"tag": "python", "rank": 3, "total": 40}]
    assert data["isMine"] is False
    assert data["speaker"] == {
        "fullName": "Ada Lovelace",
        "gender": shown_gender,
        "country": "Italy",
        "bio": "Hi",
        "grant": {"status": "Approved"},
        "proposalsCount": 2,
        "otherProposals": [{"id": str(other_proposal.id)}],
    }
    assert data["votes"] == [
        {
            "reviewerName": "Other Reviewer",
            "isMine": False,
            "scoreLabel": None,
            "scoreValue": None,
            "comment": "Not my area",
        },
        {
            "reviewerName": reviewer.full_name,
            "isMine": True,
            "scoreLabel": "Yes",
            "scoreValue": 2,
            "comment": "Mine",
        },
    ]
    assert data["myVote"] == {"scoreOptionId": str(yes.id), "comment": "Mine"}


@pytest.mark.parametrize("case", ["cancelled", "another_conference"])
def test_review_proposal_not_found(
    admin_graphql_api_client, make_reviewer, proposals_review_session, case
):
    review_session = proposals_review_session
    if case == "cancelled":
        proposal = SubmissionFactory(
            conference=review_session.conference, status="cancelled"
        )
    else:
        proposal = SubmissionFactory(conference=ConferenceFactory())
    admin_graphql_api_client.force_login(make_reviewer(review_session.conference))

    response = _review_proposal(admin_graphql_api_client, review_session, proposal)

    assert not response.get("errors")
    assert response["data"]["reviewProposal"] is None

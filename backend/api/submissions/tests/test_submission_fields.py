import pytest

from schedule.models import ScheduleItem

pytestmark = pytest.mark.django_db

QUERY = """
    query SubmissionQuery($id: ID!) {
        submission(id: $id) {
            abstract(language: "en")
            audienceLevel {
                name
            }
            elevatorPitch(language: "en")
            id
            type {
                name
            }
            topic {
                name
            }
            title(language: "en")
            tags {
                name
            }
            speakerLevel
            slug
            previousTalkVideo
            notes
            languages {
                code
            }
            duration {
                name
            }
            conference {
                code
            }
        }
    }
"""


@pytest.fixture
def other_user(user_factory):
    return user_factory()


def _submission(submission_factory, user, **kwargs):
    return submission_factory(
        speaker_id=user.id, languages=("it", "en"), tags=("python", "GraphQL"), **kwargs
    )


def _query(graphql_client, submission):
    response = graphql_client.query(
        QUERY,
        variables={"id": submission.hashid},
    )

    assert not response.get("errors")
    return response["data"]


def test_voting_open_and_user_cannot_vote(
    graphql_client, submission_factory, user, other_user, mocker
):
    submission = _submission(submission_factory, user)
    graphql_client.force_login(other_user)
    can_vote_mock = mocker.patch(
        "api.submissions.permissions.check_if_user_can_vote", return_value=False
    )

    data = _query(graphql_client, submission)

    # ✔️ public
    assert data["submission"]["title"] == submission.title.localize("en")
    assert data["submission"]["slug"] == submission.slug

    # ❌ restricted
    assert data["submission"]["elevatorPitch"] is None
    assert data["submission"]["abstract"] is None
    assert data["submission"]["topic"] is None
    assert data["submission"]["type"] is None
    assert data["submission"]["duration"] is None
    assert data["submission"]["audienceLevel"] is None
    assert data["submission"]["languages"] is None
    assert data["submission"]["tags"] is None

    # ❌ private
    assert data["submission"]["speakerLevel"] is None
    assert data["submission"]["previousTalkVideo"] is None
    assert data["submission"]["notes"] is None

    can_vote_mock.assert_called()


def test_voting_open_and_user_can_vote(
    graphql_client, submission_factory, user, other_user, mocker
):
    submission = _submission(submission_factory, user)
    graphql_client.force_login(other_user)
    can_vote_mock = mocker.patch(
        "api.submissions.permissions.check_if_user_can_vote", return_value=True
    )

    data = _query(graphql_client, submission)

    # ✔️ public
    assert data["submission"]["title"] == submission.title.localize("en")
    assert data["submission"]["slug"] == submission.slug

    # ✔️ restricted
    assert data["submission"]["elevatorPitch"] == submission.elevator_pitch.localize(
        "en"
    )
    assert data["submission"]["abstract"] == submission.abstract.localize("en")
    assert data["submission"]["topic"]["name"] == submission.topic.name
    assert data["submission"]["type"]["name"] == submission.type.name
    assert data["submission"]["duration"]["name"] == submission.duration.name
    assert data["submission"]["audienceLevel"]["name"] == submission.audience_level.name
    assert data["submission"]["languages"] == [
        {"code": "it"},
        {"code": "en"},
    ]
    assert data["submission"]["tags"] == [
        {"name": "python"},
        {"name": "GraphQL"},
    ]

    # ❌ private
    assert data["submission"]["speakerLevel"] is None
    assert data["submission"]["previousTalkVideo"] is None
    assert data["submission"]["notes"] is None

    can_vote_mock.assert_called()


def test_voring_closed_and_user_is_authenticated(
    graphql_client, other_user, submission_factory, user
):
    submission = _submission(submission_factory, user, conference__active_voting=False)
    graphql_client.force_login(other_user)

    data = _query(graphql_client, submission)

    # ✔️ public
    assert data["submission"]["title"] == submission.title.localize("en")
    assert data["submission"]["slug"] == submission.slug

    # ❌ restricted
    assert data["submission"]["elevatorPitch"] is None
    assert data["submission"]["abstract"] is None
    assert data["submission"]["topic"] is None
    assert data["submission"]["type"] is None
    assert data["submission"]["duration"] is None
    assert data["submission"]["audienceLevel"] is None
    assert data["submission"]["languages"] is None
    assert data["submission"]["tags"] is None

    # ❌ private
    assert data["submission"]["speakerLevel"] is None
    assert data["submission"]["previousTalkVideo"] is None
    assert data["submission"]["notes"] is None


def test_voring_closed_and_user_is_not_authenticated(
    graphql_client, submission_factory, user
):
    submission = _submission(submission_factory, user, conference__active_voting=False)

    data = _query(graphql_client, submission)

    # ✔️ public
    assert data["submission"]["title"] == submission.title.localize("en")
    assert data["submission"]["slug"] == submission.slug

    # ❌ restricted
    assert data["submission"]["elevatorPitch"] is None
    assert data["submission"]["abstract"] is None
    assert data["submission"]["topic"] is None
    assert data["submission"]["type"] is None
    assert data["submission"]["duration"] is None
    assert data["submission"]["audienceLevel"] is None
    assert data["submission"]["languages"] is None
    assert data["submission"]["tags"] is None

    # ❌ private
    assert data["submission"]["speakerLevel"] is None
    assert data["submission"]["previousTalkVideo"] is None
    assert data["submission"]["notes"] is None


def test_accepted_submission_user_can_see_public_and_restricted_fields(
    graphql_client, submission_factory, user, schedule_item_factory
):
    submission = _submission(submission_factory, user)
    schedule_item_factory(
        submission=submission,
        conference=submission.conference,
        type=ScheduleItem.TYPES.submission,
    )

    data = _query(graphql_client, submission)

    # ✔️ public
    assert data["submission"]["title"] == submission.title.localize("en")
    assert data["submission"]["slug"] == submission.slug

    # ✔️ restricted
    assert data["submission"]["elevatorPitch"] == submission.elevator_pitch.localize(
        "en"
    )
    assert data["submission"]["abstract"] == submission.abstract.localize("en")
    assert data["submission"]["topic"]["name"] == submission.topic.name
    assert data["submission"]["type"]["name"] == submission.type.name
    assert data["submission"]["duration"]["name"] == submission.duration.name
    assert data["submission"]["audienceLevel"]["name"] == submission.audience_level.name
    assert data["submission"]["languages"] == [
        {"code": "it"},
        {"code": "en"},
    ]
    assert data["submission"]["tags"] == [
        {"name": "python"},
        {"name": "GraphQL"},
    ]

    # ❌ private
    assert data["submission"]["speakerLevel"] is None
    assert data["submission"]["previousTalkVideo"] is None
    assert data["submission"]["notes"] is None


def test_admin_user_can_see_everything(
    graphql_client, admin_user, submission_factory, user
):
    submission = _submission(submission_factory, user)
    graphql_client.force_login(admin_user)

    data = _query(graphql_client, submission)

    # ✔️ public
    assert data["submission"]["title"] == submission.title.localize("en")
    assert data["submission"]["slug"] == submission.slug

    # ✔️ restricted
    assert data["submission"]["elevatorPitch"] == submission.elevator_pitch.localize(
        "en"
    )
    assert data["submission"]["abstract"] == submission.abstract.localize("en")
    assert data["submission"]["topic"]["name"] == submission.topic.name
    assert data["submission"]["type"]["name"] == submission.type.name
    assert data["submission"]["duration"]["name"] == submission.duration.name
    assert data["submission"]["audienceLevel"]["name"] == submission.audience_level.name
    assert data["submission"]["languages"] == [
        {"code": "it"},
        {"code": "en"},
    ]
    assert data["submission"]["tags"] == [
        {"name": "python"},
        {"name": "GraphQL"},
    ]

    # ✔️ private
    assert data["submission"]["speakerLevel"] == submission.speaker_level
    assert data["submission"]["previousTalkVideo"] == submission.previous_talk_video
    assert data["submission"]["notes"] == submission.notes


def test_submission_author_can_see_everything(graphql_client, submission_factory, user):
    submission = _submission(submission_factory, user)
    graphql_client.force_login(user)

    data = _query(graphql_client, submission)

    # ✔️ public
    assert data["submission"]["title"] == submission.title.localize("en")
    assert data["submission"]["slug"] == submission.slug

    # ✔️ restricted
    assert data["submission"]["elevatorPitch"] == submission.elevator_pitch.localize(
        "en"
    )
    assert data["submission"]["abstract"] == submission.abstract.localize("en")
    assert data["submission"]["topic"]["name"] == submission.topic.name
    assert data["submission"]["type"]["name"] == submission.type.name
    assert data["submission"]["duration"]["name"] == submission.duration.name
    assert data["submission"]["audienceLevel"]["name"] == submission.audience_level.name
    assert data["submission"]["languages"] == [
        {"code": "it"},
        {"code": "en"},
    ]
    assert data["submission"]["tags"] == [
        {"name": "python"},
        {"name": "GraphQL"},
    ]

    # ✔️ private
    assert data["submission"]["speakerLevel"] == submission.speaker_level
    assert data["submission"]["previousTalkVideo"] == submission.previous_talk_video
    assert data["submission"]["notes"] == submission.notes


def test_ranked_submission_user_can_see_public_and_restricted_fields(
    graphql_client,
    conference,
    user,
    submission_factory,
    rank_request_factory,
    mocker,
):
    mocker.patch("voting.models.ranking.get_users_data_by_ids", return_value={})
    submission = _submission(submission_factory, user=user, conference=conference)
    rank_request_factory(
        conference=conference, submissions=[submission], is_public=True
    )

    data = _query(graphql_client, submission)

    # ✔️ public
    assert data["submission"]["title"] == submission.title.localize("en")
    assert data["submission"]["slug"] == submission.slug

    # ✔️ restricted
    assert data["submission"]["elevatorPitch"] == submission.elevator_pitch.localize(
        "en"
    )
    assert data["submission"]["abstract"] == submission.abstract.localize("en")
    assert data["submission"]["topic"]["name"] == submission.topic.name
    assert data["submission"]["type"]["name"] == submission.type.name
    assert data["submission"]["duration"]["name"] == submission.duration.name
    assert data["submission"]["audienceLevel"]["name"] == submission.audience_level.name
    assert data["submission"]["languages"] == [
        {"code": "it"},
        {"code": "en"},
    ]
    assert data["submission"]["tags"] == [
        {"name": "python"},
        {"name": "GraphQL"},
    ]

    # ❌ private
    assert data["submission"]["speakerLevel"] is None
    assert data["submission"]["previousTalkVideo"] is None
    assert data["submission"]["notes"] is None


def test_ranking_is_not_public_cannot_see_restricted_and_private_fields(
    graphql_client, rank_request_factory, conference, user, submission_factory, mocker
):
    mocker.patch("voting.models.ranking.get_users_data_by_ids", return_value={})
    submission = _submission(submission_factory, user=user, conference=conference)
    rank_request_factory(
        conference=conference, submissions=[submission], is_public=False
    )

    data = _query(graphql_client, submission)

    # ✔️ public
    assert data["submission"]["title"] == submission.title.localize("en")
    assert data["submission"]["slug"] == submission.slug

    # ❌ restricted
    assert data["submission"]["elevatorPitch"] is None
    assert data["submission"]["abstract"] is None
    assert data["submission"]["topic"] is None
    assert data["submission"]["type"] is None
    assert data["submission"]["duration"] is None
    assert data["submission"]["audienceLevel"] is None
    assert data["submission"]["languages"] is None
    assert data["submission"]["tags"] is None

    # ❌ private
    assert data["submission"]["speakerLevel"] is None
    assert data["submission"]["previousTalkVideo"] is None
    assert data["submission"]["notes"] is None


def test_ranking_does_not_exists_cannot_see_restricted_and_private_fields(
    graphql_client,
    conference_factory,
    user,
    submission_factory,
):
    conference = conference_factory(rankrequest=None)
    submission = _submission(submission_factory, user=user, conference=conference)

    data = _query(graphql_client, submission)

    # ✔️ public
    assert data["submission"]["title"] == submission.title.localize("en")
    assert data["submission"]["slug"] == submission.slug

    # ❌ restricted
    assert data["submission"]["elevatorPitch"] is None
    assert data["submission"]["abstract"] is None
    assert data["submission"]["topic"] is None
    assert data["submission"]["type"] is None
    assert data["submission"]["duration"] is None
    assert data["submission"]["audienceLevel"] is None
    assert data["submission"]["languages"] is None
    assert data["submission"]["tags"] is None

    # ❌ private
    assert data["submission"]["speakerLevel"] is None
    assert data["submission"]["previousTalkVideo"] is None
    assert data["submission"]["notes"] is None

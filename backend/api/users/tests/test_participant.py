from conferences.tests.factories import ConferenceFactory
from participants.tests.factories import ParticipantFactory
from submissions.tests.factories import SubmissionFactory
from submissions.models import Submission
import pytest


pytestmark = pytest.mark.django_db


def test_user_participant(user, graphql_client):
    graphql_client.force_login(user)
    participant = ParticipantFactory(
        user_id=user.id,
        bio="biiiiio",
        photo="https://marcopycontest.blob.core.windows.net/participants-avatars/blob.jpg",
        website="https://google.it",
        twitter_handle="marco",
        speaker_level="intermediate",
        previous_talk_video="",
    )

    response = graphql_client.query(
        """query($conference: String!) {
            me {
                participant(conference: $conference) {
                    id
                    bio
                    photo
                    website
                    twitterHandle
                    speakerLevel
                    previousTalkVideo
                }
            }
        }""",
        variables={"conference": participant.conference.code},
    )

    participant_type = response["data"]["me"]["participant"]

    assert participant_type["id"] == participant.hashid
    assert participant_type["bio"] == "biiiiio"
    assert (
        participant_type["photo"]
        == "https://marcopycontest.blob.core.windows.net/participants-avatars/blob.jpg"
    )
    assert participant_type["website"] == "https://google.it"
    assert participant_type["twitterHandle"] == "marco"
    assert participant_type["speakerLevel"] == "intermediate"
    assert participant_type["previousTalkVideo"] == ""


def test_user_participant_proposals(user, graphql_client):
    graphql_client.force_login(user)
    participant = ParticipantFactory(
        user_id=user.id,
        bio="biiiiio",
        photo="https://marcopycontest.blob.core.windows.net/participants-avatars/blob.jpg",
        website="https://google.it",
        twitter_handle="marco",
        speaker_level="intermediate",
        previous_talk_video="",
    )
    proposal_1 = SubmissionFactory(
        speaker_id=participant.user_id,
        conference=participant.conference,
        status=Submission.STATUS.accepted,
    )
    SubmissionFactory(
        speaker_id=participant.user_id,
        conference=participant.conference,
        status=Submission.STATUS.rejected,
    )
    SubmissionFactory(speaker_id=participant.user_id, status=Submission.STATUS.accepted)

    response = graphql_client.query(
        """query($conference: String!) {
            me {
                participant(conference: $conference) {
                    id
                    bio
                    photo
                    website
                    twitterHandle
                    speakerLevel
                    previousTalkVideo
                    proposals {
                        id
                    }
                }
            }
        }""",
        variables={"conference": participant.conference.code},
    )

    participant_type = response["data"]["me"]["participant"]

    assert participant_type["id"] == participant.hashid
    assert len(participant_type["proposals"]) == 1
    assert participant_type["proposals"][0]["id"] == proposal_1.hashid


def test_user_participant_when_it_doesnt_exist(user, graphql_client):
    graphql_client.force_login(user)
    conference_code = ConferenceFactory().code
    response = graphql_client.query(
        """query($conference: String!) {
            me {
                participant(conference: $conference) {
                    id
                    bio
                    photo
                    website
                    twitterHandle
                    speakerLevel
                    previousTalkVideo
                }
            }
        }""",
        variables={"conference": conference_code},
    )

    assert response["data"]["me"]["participant"] is None


def test_user_participant_fails_when_not_logged_in(graphql_client):
    conference_code = ConferenceFactory().code
    response = graphql_client.query(
        """query($conference: String!) {
            me {
                participant(conference: $conference) {
                    id
                    bio
                    photo
                    website
                    twitterHandle
                    speakerLevel
                    previousTalkVideo
                }
            }
        }""",
        variables={"conference": conference_code},
    )

    assert response["errors"][0]["message"] == "User not logged in"

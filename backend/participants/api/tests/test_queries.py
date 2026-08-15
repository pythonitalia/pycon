from conferences.tests.factories import ConferenceFactory
from participants.tests.factories import ParticipantFactory


def test_query_participant(graphql_client):
    participant = ParticipantFactory()

    response = graphql_client.query(
        """
    query Participant($id: ID!, $conference: String!) {
        participant(id: $id, conference: $conference) {
            id
            fullname
        }
    }
    """,
        variables={"id": participant.hashid, "conference": participant.conference.code},
    )

    assert response["data"]["participant"]["id"] == participant.hashid
    assert response["data"]["participant"]["fullname"] == participant.user.fullname


def test_query_private_fields_of_own_user(graphql_client, user):
    graphql_client.force_login(user)
    participant = ParticipantFactory(
        user=user,
        speaker_availabilities={"test": "test"},
        previous_talk_video="test",
        speaker_level="level",
    )

    response = graphql_client.query(
        """query Participant($id: ID!, $conference: String!) {
        participant(id: $id, conference: $conference) {
            id
            speakerAvailabilities
            previousTalkVideo
            speakerLevel
        }
    }
    """,
        variables={"id": participant.hashid, "conference": participant.conference.code},
    )

    assert response["data"]["participant"]["speakerAvailabilities"] == {"test": "test"}
    assert response["data"]["participant"]["previousTalkVideo"] == "test"
    assert response["data"]["participant"]["speakerLevel"] == "level"


def test_cannot_query_private_fields_of_other_user(graphql_client):
    participant = ParticipantFactory()

    response = graphql_client.query(
        """query Participant($id: ID!, $conference: String!) {
        participant(id: $id, conference: $conference) {
            id
            speakerAvailabilities
            previousTalkVideo
            speakerLevel
        }
    }
    """,
        variables={"id": participant.hashid, "conference": participant.conference.code},
    )

    assert response["data"]["participant"]["speakerAvailabilities"] is None
    assert response["data"]["participant"]["previousTalkVideo"] is None
    assert response["data"]["participant"]["speakerLevel"] is None


def test_query_participant_with_wrong_conference(graphql_client):
    participant = ParticipantFactory()

    response = graphql_client.query(
        """
    query Participant($id: ID!, $conference: String!) {
        participant(id: $id, conference: $conference) {
            id
            fullname
        }
    }
    """,
        variables={"id": participant.hashid, "conference": ConferenceFactory().code},
    )

    assert response["data"]["participant"] is None


def test_query_participant_with_non_existent_id(graphql_client):
    response = graphql_client.query(
        """
    query Participant($id: ID!, $conference: String!) {
        participant(id: $id, conference: $conference) {
            id
            fullname
        }
    }
    """,
        variables={"id": "abcabc", "conference": ConferenceFactory().code},
    )

    assert response["data"]["participant"] is None

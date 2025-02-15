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

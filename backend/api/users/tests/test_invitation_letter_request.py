from api.visa.types import (
    InvitationLetterRequestStatus as InvitationLetterRequestStatusAPI,
)
from visa.models import InvitationLetterRequestStatus as InvitationLetterRequestStatusDB
from users.tests.factories import UserFactory
from visa.models import InvitationLetterRequestOnBehalfOf
from visa.tests.factories import InvitationLetterRequestFactory
from conferences.tests.factories import ConferenceFactory
import pytest

pytestmark = pytest.mark.django_db


def _query_invitation_letter_request(client, conference):
    return client.query(
        """query($conference: String!) {
        me {
            invitationLetterRequest(conference: $conference) {
                id
                status
            }
        }
    }""",
        variables={
            "conference": conference.code,
        },
    )


def test_get_user_invitation_letter_request_with_none_present(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory()
    response = _query_invitation_letter_request(graphql_client, conference)

    me = response["data"]["me"]
    assert me["invitationLetterRequest"] is None


def test_get_user_invitation_letter_request(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory()
    invitation_letter_request = InvitationLetterRequestFactory(
        requester=user,
        conference=conference,
    )

    response = _query_invitation_letter_request(graphql_client, conference)

    me = response["data"]["me"]
    assert me["invitationLetterRequest"]["id"] == str(invitation_letter_request.id)
    assert me["invitationLetterRequest"]["status"] == invitation_letter_request.status


@pytest.mark.parametrize(
    "actual_status,exposed_status",
    [
        (
            InvitationLetterRequestStatusDB.PENDING,
            InvitationLetterRequestStatusAPI.PENDING,
        ),
        (
            InvitationLetterRequestStatusDB.PROCESSING,
            InvitationLetterRequestStatusAPI.PENDING,
        ),
        (
            InvitationLetterRequestStatusDB.FAILED_TO_GENERATE,
            InvitationLetterRequestStatusAPI.PENDING,
        ),
        (
            InvitationLetterRequestStatusDB.PROCESSED,
            InvitationLetterRequestStatusAPI.PENDING,
        ),
        (InvitationLetterRequestStatusDB.SENT, InvitationLetterRequestStatusAPI.SENT),
        (
            InvitationLetterRequestStatusDB.REJECTED,
            InvitationLetterRequestStatusAPI.REJECTED,
        ),
    ],
)
def test_user_invitation_letter_request_has_user_friendly_status(
    graphql_client, user, actual_status, exposed_status
):
    graphql_client.force_login(user)

    conference = ConferenceFactory()
    invitation_letter_request = InvitationLetterRequestFactory(
        requester=user, conference=conference, status=actual_status
    )

    response = _query_invitation_letter_request(graphql_client, conference)

    me = response["data"]["me"]
    assert me["invitationLetterRequest"]["id"] == str(invitation_letter_request.id)
    assert me["invitationLetterRequest"]["status"] == exposed_status.name


def test_on_behalf_of_others_invitation_letter_request_are_excluded(
    graphql_client, user
):
    graphql_client.force_login(user)

    conference = ConferenceFactory()

    InvitationLetterRequestFactory(
        requester=user,
        conference=conference,
        on_behalf_of=InvitationLetterRequestOnBehalfOf.OTHER,
    )

    InvitationLetterRequestFactory(
        requester=user,
        conference=conference,
        on_behalf_of=InvitationLetterRequestOnBehalfOf.OTHER,
    )

    response = _query_invitation_letter_request(graphql_client, conference)

    me = response["data"]["me"]
    assert me["invitationLetterRequest"] is None


def test_other_users_invitation_letter_requests_are_excluded(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory()

    InvitationLetterRequestFactory(
        requester=UserFactory(),
        conference=conference,
        on_behalf_of=InvitationLetterRequestOnBehalfOf.SELF,
    )

    response = _query_invitation_letter_request(graphql_client, conference)

    me = response["data"]["me"]
    assert me["invitationLetterRequest"] is None


def test_other_conferences_invitation_letter_request_are_excluded(graphql_client, user):
    graphql_client.force_login(user)

    conference = ConferenceFactory()

    InvitationLetterRequestFactory(
        requester=user,
        conference=ConferenceFactory(),
        on_behalf_of=InvitationLetterRequestOnBehalfOf.SELF,
    )

    response = _query_invitation_letter_request(graphql_client, conference)

    me = response["data"]["me"]
    assert me["invitationLetterRequest"] is None

from privacy_policy.models import PrivacyPolicyAcceptanceRecord

from datetime import date
from api.visa.mutations.request_invitation_letter import MAX_LENGTH_FIELDS
from visa.tests.factories import InvitationLetterRequestFactory
from visa.models import (
    InvitationLetterRequest,
    InvitationLetterRequestOnBehalfOf,
    InvitationLetterRequestStatus,
)
from conferences.tests.factories import ConferenceFactory
import pytest

pytestmark = pytest.mark.django_db


def _request_invitation_letter(client, **input):
    return client.query(
        """mutation RequestInvitationLetter($input: RequestInvitationLetterInput!) {
        requestInvitationLetter(input: $input) {
            __typename

            ... on InvitationLetterRequest {
                id
                status
            }

            ... on RequestInvitationLetterErrors {
                errors {
                    address
                    conference
                    dateOfBirth
                    email
                    embassyName
                    fullName
                    nationality
                    onBehalfOf
                    passportNumber
                }
            }
        }
    }""",
        variables=input,
    )


def test_request_invitation_letter(graphql_client, user, mock_has_ticket):
    conference = ConferenceFactory()
    mock_has_ticket(conference)

    graphql_client.force_login(user)

    response = _request_invitation_letter(
        graphql_client,
        input={
            "conference": conference.code,
            "onBehalfOf": "SELF",
            "fullName": "Mario Rossi",
            "email": "",
            "nationality": "Italian",
            "address": "via Roma",
            "passportNumber": "YA1234567",
            "embassyName": "Italian Embassy in France",
            "dateOfBirth": "1999-01-01",
        },
    )

    assert (
        response["data"]["requestInvitationLetter"]["__typename"]
        == "InvitationLetterRequest"
    )
    assert response["data"]["requestInvitationLetter"]["status"] == "PENDING"

    invitation_letter_request = InvitationLetterRequest.objects.get()

    assert response["data"]["requestInvitationLetter"]["id"] == str(
        invitation_letter_request.id
    )

    assert invitation_letter_request.requester == user
    assert invitation_letter_request.conference == conference
    assert (
        invitation_letter_request.on_behalf_of == InvitationLetterRequestOnBehalfOf.SELF
    )
    assert invitation_letter_request.full_name == "Mario Rossi"
    assert invitation_letter_request.email_address == ""
    assert invitation_letter_request.nationality == "Italian"
    assert invitation_letter_request.address == "via Roma"
    assert invitation_letter_request.passport_number == "YA1234567"
    assert invitation_letter_request.embassy_name == "Italian Embassy in France"
    assert invitation_letter_request.date_of_birth == date(1999, 1, 1)
    assert invitation_letter_request.status == InvitationLetterRequestStatus.PENDING
    assert PrivacyPolicyAcceptanceRecord.objects.filter(
        user=user, conference=conference, privacy_policy="invitation_letter"
    ).exists()


def test_can_request_invitation_letter_to_multiple_conferences(
    graphql_client, user, mock_has_ticket
):
    graphql_client.force_login(user)

    conference = ConferenceFactory()
    mock_has_ticket(conference)

    InvitationLetterRequestFactory(
        requester=user,
        conference=conference,
        on_behalf_of=InvitationLetterRequestOnBehalfOf.SELF,
    )

    other_conference = ConferenceFactory()
    mock_has_ticket(other_conference)

    response = _request_invitation_letter(
        graphql_client,
        input={
            "conference": other_conference.code,
            "onBehalfOf": "SELF",
            "fullName": "Mario Rossi",
            "email": "",
            "nationality": "Italian",
            "address": "via Roma",
            "passportNumber": "YA1234567",
            "embassyName": "Italian Embassy in France",
            "dateOfBirth": "1999-01-01",
        },
    )

    assert (
        response["data"]["requestInvitationLetter"]["__typename"]
        == "InvitationLetterRequest"
    )
    assert response["data"]["requestInvitationLetter"]["status"] == "PENDING"

    invitation_letter_request = InvitationLetterRequest.objects.filter(
        requester=user,
        conference=other_conference,
    ).get()

    assert response["data"]["requestInvitationLetter"]["id"] == str(
        invitation_letter_request.id
    )

    assert invitation_letter_request.requester == user
    assert invitation_letter_request.conference == other_conference
    assert (
        invitation_letter_request.on_behalf_of == InvitationLetterRequestOnBehalfOf.SELF
    )
    assert invitation_letter_request.full_name == "Mario Rossi"
    assert invitation_letter_request.email_address == ""
    assert invitation_letter_request.nationality == "Italian"
    assert invitation_letter_request.address == "via Roma"
    assert invitation_letter_request.passport_number == "YA1234567"
    assert invitation_letter_request.embassy_name == "Italian Embassy in France"
    assert invitation_letter_request.date_of_birth == date(1999, 1, 1)
    assert invitation_letter_request.status == InvitationLetterRequestStatus.PENDING
    assert PrivacyPolicyAcceptanceRecord.objects.filter(
        user=user, conference=other_conference, privacy_policy="invitation_letter"
    ).exists()


def test_request_invitation_letter_email_is_ignored_for_self_requests(
    graphql_client, user, mock_has_ticket
):
    conference = ConferenceFactory()
    mock_has_ticket(conference)

    graphql_client.force_login(user)

    response = _request_invitation_letter(
        graphql_client,
        input={
            "conference": conference.code,
            "onBehalfOf": "SELF",
            "fullName": "Mario Rossi",
            "email": "ignored@example.com",
            "nationality": "Italian",
            "address": "via Roma",
            "passportNumber": "YA1234567",
            "embassyName": "Italian Embassy in France",
            "dateOfBirth": "1999-01-01",
        },
    )

    assert (
        response["data"]["requestInvitationLetter"]["__typename"]
        == "InvitationLetterRequest"
    )
    assert response["data"]["requestInvitationLetter"]["status"] == "PENDING"

    invitation_letter_request = InvitationLetterRequest.objects.get()

    assert response["data"]["requestInvitationLetter"]["id"] == str(
        invitation_letter_request.id
    )

    assert invitation_letter_request.requester == user
    assert invitation_letter_request.conference == conference
    assert (
        invitation_letter_request.on_behalf_of == InvitationLetterRequestOnBehalfOf.SELF
    )
    assert invitation_letter_request.full_name == "Mario Rossi"
    assert invitation_letter_request.email_address == ""


@pytest.mark.parametrize("has_ticket", [True, False])
def test_request_invitation_letter_on_behalf_of_other(
    graphql_client, user, mock_has_ticket, has_ticket
):
    conference = ConferenceFactory()
    mock_has_ticket(conference, has_ticket=has_ticket, user=user)

    graphql_client.force_login(user)

    response = _request_invitation_letter(
        graphql_client,
        input={
            "conference": conference.code,
            "onBehalfOf": "OTHER",
            "fullName": "Jane Doe",
            "email": "other@example.com",
            "nationality": "Italian",
            "address": "via Roma",
            "passportNumber": "YA1234567",
            "embassyName": "Italian Embassy in London",
            "dateOfBirth": "1995-12-03",
        },
    )

    assert (
        response["data"]["requestInvitationLetter"]["__typename"]
        == "InvitationLetterRequest"
    )
    assert response["data"]["requestInvitationLetter"]["status"] == "PENDING"

    invitation_letter_request = InvitationLetterRequest.objects.get()

    assert response["data"]["requestInvitationLetter"]["id"] == str(
        invitation_letter_request.id
    )

    assert invitation_letter_request.requester == user
    assert invitation_letter_request.conference == conference
    assert (
        invitation_letter_request.on_behalf_of
        == InvitationLetterRequestOnBehalfOf.OTHER
    )
    assert invitation_letter_request.full_name == "Jane Doe"
    assert invitation_letter_request.email_address == "other@example.com"
    assert invitation_letter_request.nationality == "Italian"
    assert invitation_letter_request.address == "via Roma"
    assert invitation_letter_request.passport_number == "YA1234567"
    assert invitation_letter_request.embassy_name == "Italian Embassy in London"
    assert invitation_letter_request.date_of_birth == date(1995, 12, 3)
    assert invitation_letter_request.status == InvitationLetterRequestStatus.PENDING


def test_duplicate_requests_for_others_are_ignored(
    graphql_client, user, mock_has_ticket
):
    conference = ConferenceFactory()
    mock_has_ticket(conference, has_ticket=True, user=user)

    graphql_client.force_login(user)

    input = {
        "conference": conference.code,
        "onBehalfOf": "OTHER",
        "fullName": "Jane Doe",
        "email": "other@example.com",
        "nationality": "Italian",
        "address": "via Roma",
        "passportNumber": "YA1234567",
        "embassyName": "Italian Embassy in London",
        "dateOfBirth": "1995-12-03",
    }

    response = _request_invitation_letter(
        graphql_client,
        input=input,
    )

    assert (
        response["data"]["requestInvitationLetter"]["__typename"]
        == "InvitationLetterRequest"
    )
    assert response["data"]["requestInvitationLetter"]["status"] == "PENDING"

    invitation_letter_request = InvitationLetterRequest.objects.get()
    assert response["data"]["requestInvitationLetter"]["id"] == str(
        invitation_letter_request.id
    )

    response = _request_invitation_letter(
        graphql_client,
        input=input,
    )

    assert (
        response["data"]["requestInvitationLetter"]["__typename"]
        == "InvitationLetterRequest"
    )
    assert response["data"]["requestInvitationLetter"]["status"] == "PENDING"
    assert response["data"]["requestInvitationLetter"]["id"] == str(
        invitation_letter_request.id
    )
    assert InvitationLetterRequest.objects.count() == 1
    assert (
        PrivacyPolicyAcceptanceRecord.objects.filter(
            user=user, conference=conference, privacy_policy="invitation_letter"
        ).count()
        == 1
    )


def test_cannot_request_invitation_letter_if_already_done(
    graphql_client, user, mock_has_ticket
):
    conference = ConferenceFactory()
    mock_has_ticket(conference)

    InvitationLetterRequestFactory(
        requester=user,
        conference=conference,
    )

    graphql_client.force_login(user)

    response = _request_invitation_letter(
        graphql_client,
        input={
            "conference": conference.code,
            "onBehalfOf": "SELF",
            "fullName": "Mario Rossi",
            "email": "",
            "nationality": "Italian",
            "address": "via Roma",
            "passportNumber": "YA1234567",
            "embassyName": "Italian Embassy in France",
            "dateOfBirth": "1999-01-01",
        },
    )

    assert (
        response["data"]["requestInvitationLetter"]["__typename"]
        == "InvitationLetterAlreadyRequested"
    )
    assert InvitationLetterRequest.objects.count() == 1


def test_cannot_request_invitation_letter_without_ticket(
    graphql_client, user, mock_has_ticket
):
    conference = ConferenceFactory()
    mock_has_ticket(conference, False)

    graphql_client.force_login(user)

    response = _request_invitation_letter(
        graphql_client,
        input={
            "conference": conference.code,
            "onBehalfOf": "SELF",
            "fullName": "Mario Rossi",
            "email": "",
            "nationality": "Italian",
            "address": "via Roma",
            "passportNumber": "YA1234567",
            "embassyName": "Italian Embassy in France",
            "dateOfBirth": "1999-01-01",
        },
    )

    assert (
        response["data"]["requestInvitationLetter"]["__typename"] == "NoAdmissionTicket"
    )
    assert InvitationLetterRequest.objects.count() == 0


def test_cannot_request_invitation_letter_for_non_existing_conference(
    graphql_client, user, mock_has_ticket
):
    conference = ConferenceFactory()
    mock_has_ticket(conference)

    graphql_client.force_login(user)

    response = _request_invitation_letter(
        graphql_client,
        input={
            "conference": "non-existing",
            "onBehalfOf": "SELF",
            "fullName": "Mario Rossi",
            "email": "",
            "nationality": "Italian",
            "address": "via Roma",
            "passportNumber": "YA1234567",
            "embassyName": "Italian Embassy in France",
            "dateOfBirth": "1999-01-01",
        },
    )

    assert (
        response["data"]["requestInvitationLetter"]["__typename"]
        == "RequestInvitationLetterErrors"
    )
    assert response["data"]["requestInvitationLetter"]["errors"]["conference"] == [
        "Conference not found"
    ]
    assert InvitationLetterRequest.objects.count() == 0


def test_email_is_required_when_requesting_on_behalf_of_other(
    graphql_client, user, mock_has_ticket
):
    conference = ConferenceFactory()
    mock_has_ticket(conference, has_ticket=True, user=user)

    graphql_client.force_login(user)

    response = _request_invitation_letter(
        graphql_client,
        input={
            "conference": conference.code,
            "onBehalfOf": "OTHER",
            "fullName": "Mario Rossi",
            "email": "",
            "nationality": "Italian",
            "address": "via Roma",
            "passportNumber": "YA1234567",
            "embassyName": "Italian Embassy in France",
            "dateOfBirth": "1999-01-01",
        },
    )

    assert (
        response["data"]["requestInvitationLetter"]["__typename"]
        == "RequestInvitationLetterErrors"
    )
    assert response["data"]["requestInvitationLetter"]["errors"]["email"] == [
        "This field is required"
    ]
    assert InvitationLetterRequest.objects.count() == 0


def test_required_fields_are_enforced(graphql_client, user, mock_has_ticket):
    conference = ConferenceFactory()
    mock_has_ticket(conference, has_ticket=True, user=user)

    graphql_client.force_login(user)

    response = _request_invitation_letter(
        graphql_client,
        input={
            "conference": conference.code,
            "onBehalfOf": "SELF",
            "fullName": "",
            "email": "",
            "nationality": "",
            "address": "",
            "passportNumber": "",
            "embassyName": "",
            "dateOfBirth": "1992-10-10",
        },
    )

    assert (
        response["data"]["requestInvitationLetter"]["__typename"]
        == "RequestInvitationLetterErrors"
    )
    assert response["data"]["requestInvitationLetter"]["errors"] == {
        "conference": [],
        "address": ["This field is required"],
        "embassyName": ["This field is required"],
        "fullName": ["This field is required"],
        "passportNumber": ["This field is required"],
        "nationality": ["This field is required"],
        "dateOfBirth": [],
        "onBehalfOf": [],
        "email": [],
    }
    assert InvitationLetterRequest.objects.count() == 0


def test_max_lengths_are_enforced(graphql_client, user, mock_has_ticket):
    conference = ConferenceFactory()
    mock_has_ticket(conference, has_ticket=True, user=user)

    graphql_client.force_login(user)

    response = _request_invitation_letter(
        graphql_client,
        input={
            "conference": conference.code,
            "onBehalfOf": "SELF",
            "fullName": "a" * (MAX_LENGTH_FIELDS["full_name"] + 1),
            "email": "a" * (MAX_LENGTH_FIELDS["email"] + 1),
            "nationality": "a" * (MAX_LENGTH_FIELDS["nationality"] + 1),
            "address": "a" * (MAX_LENGTH_FIELDS["address"] + 1),
            "passportNumber": "a" * (MAX_LENGTH_FIELDS["passport_number"] + 1),
            "embassyName": "a" * (MAX_LENGTH_FIELDS["embassy_name"] + 1),
            "dateOfBirth": "1992-10-10",
        },
    )

    assert (
        response["data"]["requestInvitationLetter"]["__typename"]
        == "RequestInvitationLetterErrors"
    )
    assert response["data"]["requestInvitationLetter"]["errors"] == {
        "conference": [],
        "address": [
            f"Ensure this field has no more than {MAX_LENGTH_FIELDS['address']} characters"
        ],
        "embassyName": [
            f"Ensure this field has no more than {MAX_LENGTH_FIELDS['embassy_name']} characters"
        ],
        "fullName": [
            f"Ensure this field has no more than {MAX_LENGTH_FIELDS['full_name']} characters"
        ],
        "passportNumber": [
            f"Ensure this field has no more than {MAX_LENGTH_FIELDS['passport_number']} characters"
        ],
        "nationality": [
            f"Ensure this field has no more than {MAX_LENGTH_FIELDS['nationality']} characters"
        ],
        "dateOfBirth": [],
        "onBehalfOf": [],
        "email": [
            f"Ensure this field has no more than {MAX_LENGTH_FIELDS['email']} characters",
            "Invalid email address",
        ],
    }
    assert InvitationLetterRequest.objects.count() == 0

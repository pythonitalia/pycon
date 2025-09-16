from privacy_policy.models import PrivacyPolicyAcceptanceRecord
from conferences.tests.factories import ConferenceFactory
from grants.tests.factories import GrantFactory
import pytest
from participants.models import Participant
from grants.models import Grant
from notifications.models import EmailTemplateIdentifier
from notifications.tests.factories import EmailTemplateFactory


pytestmark = pytest.mark.django_db


def _send_grant(client, conference, conference_code=None, **kwargs):
    grant = GrantFactory.build(conference=conference)
    document = """
        mutation SendGrant($input: SendGrantInput!) {
            sendGrant(input: $input) {
                __typename

                ... on Grant {
                    id
                }

                ... on GrantErrors {
                    errors {
                        validationConference: conference
                        validationName: name
                        validationFullName: fullName
                        validationGender: gender
                        validationGrantType: grantType
                        validationOccupation: occupation
                        validationAgeGroup: ageGroup
                        validationPythonUsage: pythonUsage
                        validationCommunityContribution: communityContribution
                        validationBeenToOtherEvents: beenToOtherEvents
                        validationNeedsFundsForTravel: needsFundsForTravel
                        validationNeedVisa: needVisa
                        validationNeedAccommodation: needAccommodation
                        validationWhy: why
                        validationNotes: notes
                        validationDepartureCountry: departureCountry
                        validationNationality: nationality
                        validationDepartureCity: departureCity
                        validationParticipantBio: participantBio
                        validationParticipantWebsite: participantWebsite
                        validationParticipantTwitterHandle: participantTwitterHandle
                        validationparticipantInstagramHandle: participantInstagramHandle
                        validationParticipantLinkedinUrl: participantLinkedinUrl
                        validationParticipantFacebookUrl: participantFacebookUrl
                        validationParticipantMastodonHandle: participantMastodonHandle
                        nonFieldErrors
                    }
                }
            }
        }
    """

    defaults = {
        "name": grant.name,
        "fullName": grant.full_name,
        "conference": conference_code or conference.code,
        "ageGroup": grant.age_group,
        "gender": grant.gender,
        "occupation": grant.occupation,
        "grantType": grant.grant_type,
        "pythonUsage": grant.python_usage,
        "communityContribution": grant.community_contribution,
        "beenToOtherEvents": grant.been_to_other_events,
        "needsFundsForTravel": grant.needs_funds_for_travel,
        "needVisa": grant.need_visa,
        "needAccommodation": grant.need_accommodation,
        "why": grant.why,
        "notes": grant.notes,
        "departureCountry": grant.departure_country,
        "nationality": grant.nationality,
        "departureCity": grant.departure_city,
        "participantBio": "my bio",
        "participantWebsite": "http://website.it",
        "participantTwitterHandle": "handle",
        "participantInstagramHandle": "handleinsta",
        "participantLinkedinUrl": "https://linkedin.com/fake-link",
        "participantFacebookUrl": "https://facebook.com/fake-link",
        "participantMastodonHandle": "fake@mastodon.social",
    }

    variables = {**defaults, **kwargs}

    response = client.query(document, variables={"input": variables})

    return response


def test_send_grant(graphql_client, user, mocker, django_capture_on_commit_callbacks, sent_emails):
    graphql_client.force_login(user)
    conference = ConferenceFactory(active_grants=True)
    EmailTemplateFactory(
        conference=conference,
        identifier=EmailTemplateIdentifier.grant_application_confirmation,
    )

    with django_capture_on_commit_callbacks(execute=True):
        response = _send_grant(graphql_client, conference)

    # The API response is successful
    assert response["data"]["sendGrant"]["__typename"] == "Grant"
    assert response["data"]["sendGrant"]["id"]

    # A participant is created
    participant = Participant.objects.get(conference=conference, user_id=user.id)
    assert participant.bio == "my bio"

    # A grant object is created
    grant = Grant.objects.get(id=response["data"]["sendGrant"]["id"])
    assert grant.conference == conference
    assert PrivacyPolicyAcceptanceRecord.objects.filter(
        user=user, conference=conference, privacy_policy="grant"
    ).exists()

    # Verify that the correct email template was used and email was sent
    emails_sent = sent_emails()
    assert emails_sent.count() == 1
    
    sent_email = emails_sent.first()
    assert sent_email.email_template.identifier == EmailTemplateIdentifier.grant_application_confirmation
    assert sent_email.email_template.conference == conference
    assert sent_email.recipient == user
    assert sent_email.recipient_email == user.email
    
    # Verify placeholders were processed correctly
    assert sent_email.placeholders["user_name"] == user.full_name


def test_cannot_send_a_grant_if_grants_are_closed(graphql_client, user, mocker):
    graphql_client.force_login(user)
    conference = ConferenceFactory(active_grants=False)

    response = _send_grant(graphql_client, conference)

    assert not response.get("errors")
    assert response["data"]["sendGrant"]["__typename"] == "GrantErrors"
    assert response["data"]["sendGrant"]["errors"]["nonFieldErrors"] == [
        "The grants form is not open!"
    ]


def test_cannot_send_a_grant_if_grants_deadline_do_not_exists(graphql_client, user):
    conference = ConferenceFactory()
    assert list(conference.deadlines.all()) == []
    graphql_client.force_login(user)

    response = _send_grant(graphql_client, conference)

    assert not response.get("errors")
    assert response["data"]["sendGrant"]["__typename"] == "GrantErrors"
    assert response["data"]["sendGrant"]["errors"]["nonFieldErrors"] == [
        "The grants form is not open!"
    ]


def test_cannot_send_a_grant_as_unlogged_user(graphql_client):
    conference = ConferenceFactory()

    resp = _send_grant(graphql_client, conference)

    assert resp["errors"][0]["message"] == "User not logged in"


def test_cannot_send_two_grants_to_the_same_conference(graphql_client, user, mocker):
    graphql_client.force_login(user)
    conference = ConferenceFactory(active_grants=True)
    EmailTemplateFactory(
        conference=conference,
        identifier=EmailTemplateIdentifier.grant_application_confirmation,
    )
    _send_grant(graphql_client, conference)

    response = _send_grant(graphql_client, conference)

    assert not response.get("errors")
    assert response["data"]["sendGrant"]["__typename"] == "GrantErrors"
    assert response["data"]["sendGrant"]["errors"]["nonFieldErrors"] == [
        "Grant already submitted!"
    ]


def test_can_send_two_grants_to_different_conferences(
    graphql_client, user, mocker, django_capture_on_commit_callbacks
):
    graphql_client.force_login(user)
    conference = ConferenceFactory(active_grants=True)
    conference_2 = ConferenceFactory(active_grants=True)
    EmailTemplateFactory(
        conference=conference,
        identifier=EmailTemplateIdentifier.grant_application_confirmation,
    )
    EmailTemplateFactory(
        conference=conference_2,
        identifier=EmailTemplateIdentifier.grant_application_confirmation,
    )
    first_response = _send_grant(graphql_client, conference)
    assert not first_response.get("errors")
    assert first_response["data"]["sendGrant"]["__typename"] == "Grant"

    second_response = _send_grant(graphql_client, conference_2)

    assert not second_response.get("errors")
    assert second_response["data"]["sendGrant"]["__typename"] == "Grant"


def test_invalid_conference(graphql_client, user):
    graphql_client.force_login(user)

    response = _send_grant(
        graphql_client, ConferenceFactory(), conference_code="invalid"
    )

    assert not response.get("errors")
    assert response["data"]["sendGrant"]["__typename"] == "GrantErrors"
    assert response["data"]["sendGrant"]["errors"]["validationConference"] == [
        "Invalid conference"
    ]


def test_cannot_send_grant_outside_allowed_values(
    graphql_client,
    user,
):
    graphql_client.force_login(user)
    conference = ConferenceFactory(
        active_grants=True,
    )

    response = _send_grant(
        graphql_client,
        conference,
        name="Marcotte" * 50,
        departureCountry="Very long location" * 50,
        nationality="Freedonia" * 50,
        departureCity="Emerald City " * 50,
    )

    assert response["data"]["sendGrant"]["__typename"] == "GrantErrors"
    assert response["data"]["sendGrant"]["errors"]["validationName"] == [
        "name: Cannot be more than 300 chars"
    ]
    assert response["data"]["sendGrant"]["errors"]["validationDepartureCountry"] == [
        "departure_country: Cannot be more than 100 chars"
    ]
    assert response["data"]["sendGrant"]["errors"]["validationNationality"] == [
        "nationality: Cannot be more than 100 chars"
    ]
    assert response["data"]["sendGrant"]["errors"]["validationDepartureCity"] == [
        "departure_city: Cannot be more than 100 chars"
    ]


def test_cannot_send_grant_with_empty_values(
    graphql_client,
    user,
):
    graphql_client.force_login(user)
    conference = ConferenceFactory(
        active_grants=True,
    )

    response = _send_grant(
        graphql_client,
        conference,
        fullName="",
        pythonUsage="",
        beenToOtherEvents="",
        why="",
    )

    assert response["data"]["sendGrant"]["__typename"] == "GrantErrors"
    assert response["data"]["sendGrant"]["errors"]["validationFullName"] == [
        "full_name: Cannot be empty"
    ]


def test_submit_grant_with_existing_participant(graphql_client, user):
    graphql_client.force_login(user)
    conference = ConferenceFactory(
        active_grants=True,
    )
    EmailTemplateFactory(
        conference=conference,
        identifier=EmailTemplateIdentifier.grant_application_confirmation,
    )
    participant = Participant.objects.create(
        conference=conference, user_id=user.id, bio="old bio"
    )

    response = _send_grant(
        graphql_client,
        conference,
        participantBio="my bio",
        participantWebsite="https://sushi.com",
    )

    assert response["data"]["sendGrant"]["__typename"] == "Grant"
    assert response["data"]["sendGrant"]["id"]

    grant = Grant.objects.get(id=response["data"]["sendGrant"]["id"])
    assert grant.status == Grant.Status.pending
    assert grant.conference == conference
    assert grant.user_id == user.id

    participant.refresh_from_db()
    assert participant.bio == "my bio"
    assert participant.website == "https://sushi.com"

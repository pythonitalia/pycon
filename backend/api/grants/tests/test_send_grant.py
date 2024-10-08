from privacy_policy.models import PrivacyPolicyAcceptanceRecord
from conferences.tests.factories import ConferenceFactory
from grants.tests.factories import GrantFactory
import pytest

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
                        validationInterestedInVolunteering: interestedInVolunteering
                        validationNeedsFundsForTravel: needsFundsForTravel
                        validationNeedVisa: needVisa
                        validationNeedAccommodation: needAccommodation
                        validationWhy: why
                        validationNotes: notes
                        validationTravellingFrom: travellingFrom
                        validationWebsite: website
                        validationTwitterHandle: twitterHandle
                        validationGithubHandle: githubHandle
                        validationLinkedinUrl: linkedinUrl
                        validationMastodonHandle: mastodonHandle
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
        "interestedInVolunteering": grant.interested_in_volunteering,
        "needsFundsForTravel": grant.needs_funds_for_travel,
        "needVisa": grant.need_visa,
        "needAccommodation": grant.need_accommodation,
        "why": grant.why,
        "notes": grant.notes,
        "travellingFrom": grant.travelling_from,
        "website": grant.website,
        "twitterHandle": grant.twitter_handle,
        "githubHandle": grant.github_handle,
        "linkedinUrl": grant.linkedin_url,
        "mastodonHandle": grant.mastodon_handle,
    }

    variables = {**defaults, **kwargs}

    response = client.query(document, variables={"input": variables})

    return response


def test_send_grant(graphql_client, user):
    graphql_client.force_login(user)
    conference = ConferenceFactory(active_grants=True)

    response = _send_grant(graphql_client, conference)

    assert response["data"]["sendGrant"]["__typename"] == "Grant"
    assert response["data"]["sendGrant"]["id"]

    assert PrivacyPolicyAcceptanceRecord.objects.filter(
        user=user, conference=conference, privacy_policy="grant"
    ).exists()


def test_cannot_send_a_grant_if_grants_are_closed(graphql_client, user):
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


def test_cannot_send_two_grants_to_the_same_conference(graphql_client, user):
    graphql_client.force_login(user)
    conference = ConferenceFactory(active_grants=True)
    _send_grant(graphql_client, conference)

    response = _send_grant(graphql_client, conference)

    assert not response.get("errors")
    assert response["data"]["sendGrant"]["__typename"] == "GrantErrors"
    assert response["data"]["sendGrant"]["errors"]["nonFieldErrors"] == [
        "Grant already submitted!"
    ]


def test_can_send_two_grants_to_different_conferences(graphql_client, user):
    graphql_client.force_login(user)
    conference = ConferenceFactory(active_grants=True)
    conference_2 = ConferenceFactory(active_grants=True)
    _send_grant(graphql_client, conference)

    response = _send_grant(graphql_client, conference_2)

    assert not response.get("errors")
    assert response["data"]["sendGrant"]["__typename"] == "Grant"


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
        travellingFrom="Very long location" * 50,
    )

    assert response["data"]["sendGrant"]["__typename"] == "GrantErrors"
    assert response["data"]["sendGrant"]["errors"]["validationName"] == [
        "name: Cannot be more than 300 chars"
    ]
    assert response["data"]["sendGrant"]["errors"]["validationTravellingFrom"] == [
        "travelling_from: Cannot be more than 200 chars"
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

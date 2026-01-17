from users.tests.factories import UserFactory
from django.contrib.admin.models import LogEntry
from conferences.tests.factories import ConferenceFactory
from grants.tests.factories import GrantFactory
import pytest
from participants.models import Participant

pytestmark = pytest.mark.django_db


def _update_grant(graphql_client, grant, **kwargs):
    query = """
    mutation updateGrant($input: UpdateGrantInput!){
        updateGrant(input: $input) {
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
                    validationParticipantInstagramHandle: participantInstagramHandle
                    validationParticipantLinkedinUrl: participantLinkedinUrl
                    validationParticipantFacebookUrl: participantFacebookUrl
                    validationparticipantMastodonHandle: participantMastodonHandle
                    nonFieldErrors
                }
            }
        }
    }
    """

    defaults = {
        "name": grant.name,
        "fullName": grant.full_name,
        "conference": grant.conference.code,
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
        "participantBio": "bio",
        "participantWebsite": "http://website.it",
        "participantTwitterHandle": "handle",
        "participantInstagramHandle": "handleinsta",
        "participantLinkedinUrl": "https://linkedin.com/fake-link",
        "participantFacebookUrl": "https://facebook.com/fake-link",
        "participantMastodonHandle": "fake@mastodon.social",
    }

    variables = {
        **defaults,
        **kwargs,
        "conference": grant.conference.code,
        "instance": grant.id,
    }

    response = graphql_client.query(query, variables={"input": variables})

    return response


def test_update_grant(graphql_client, user):
    graphql_client.force_login(user)
    conference = ConferenceFactory(active_grants=True)
    grant = GrantFactory(conference=conference, gender="female", user_id=user.id)

    response = _update_grant(
        graphql_client,
        grant,
        name="Marcotte",
        fullName="Marcotte B. A.",
        ageGroup="range_25_34",
        gender="male",
        occupation="student",
        grantType="diversity",
        pythonUsage="random",
        communityContribution="Soft toys meetups",
        beenToOtherEvents="no",
        needsFundsForTravel=True,
        needVisa=True,
        needAccommodation=True,
        why="why not",
        notes="🧸",
        departureCountry="GB",
        nationality="Italian",
        departureCity="Rome",
        participantFacebookUrl="http://facebook.com/pythonpizza",
        participantLinkedinUrl="http://linkedin.com/company/pythonpizza",
    )

    grant.refresh_from_db()

    assert not response.get("errors")
    assert response["data"]["updateGrant"]["__typename"] == "Grant"

    participant = Participant.objects.first()
    assert participant.facebook_url == "http://facebook.com/pythonpizza"
    assert participant.linkedin_url == "http://linkedin.com/company/pythonpizza"

    assert LogEntry.objects.count() == 1
    log_entry = LogEntry.objects.first()
    assert log_entry.user_id == user.id
    assert log_entry.user == user
    assert log_entry.object_id == str(grant.id)
    assert log_entry.change_message == "Grant updated"


def test_cannot_update_a_grant_if_user_is_not_owner(
    graphql_client,
    user,
):
    other_user = UserFactory()
    conference = ConferenceFactory(active_grants=True)
    grant = GrantFactory(conference=conference, user_id=user.id)
    graphql_client.force_login(other_user)

    response = _update_grant(
        graphql_client,
        grant,
        name="Marcotte",
    )

    assert response["data"]["updateGrant"]["__typename"] == "GrantErrors"
    assert response["data"]["updateGrant"]["errors"]["nonFieldErrors"] == [
        "You cannot edit this grant"
    ]


def test_cannot_update_a_grant_if_grants_are_closed(
    graphql_client,
    user,
):
    graphql_client.force_login(user)
    conference = ConferenceFactory(active_grants=False)
    grant = GrantFactory(conference=conference, user_id=user.id)

    response = _update_grant(
        graphql_client,
        grant,
        name="Marcotte",
    )

    assert response["data"]["updateGrant"]["__typename"] == "GrantErrors"
    assert response["data"]["updateGrant"]["errors"]["nonFieldErrors"] == [
        "The grants form is not open!"
    ]


def test_cannot_update_a_grant_if_grants_deadline_do_not_exists(graphql_client, user):
    conference = ConferenceFactory()
    assert list(conference.deadlines.all()) == []
    graphql_client.force_login(user)
    grant = GrantFactory(conference=conference, user_id=user.id)

    response = _update_grant(graphql_client, grant)

    assert not response.get("errors")
    assert response["data"]["updateGrant"]["__typename"] == "GrantErrors"
    assert response["data"]["updateGrant"]["errors"]["nonFieldErrors"] == [
        "The grants form is not open!"
    ]


def test_cannot_update_a_grant_as_unlogged_user(graphql_client):
    grant = GrantFactory()
    resp = _update_grant(graphql_client, grant)

    assert resp["errors"][0]["message"] == "User not logged in"


def test_cannot_update_grant_outside_allowed_values(
    graphql_client,
    user,
):
    graphql_client.force_login(user)
    conference = ConferenceFactory(
        active_grants=True,
    )

    grant = GrantFactory(
        user_id=user.id,
        conference=conference,
    )

    response = _update_grant(
        graphql_client,
        grant=grant,
        name="Marcotte" * 50,
        fullName="Marcotte" * 50,
        departureCountry="Very long location" * 50,
        nationality="Freedonia" * 50,
        departureCity="Emerald City " * 50,
        why="Very long why" * 100,
        pythonUsage="Very long python usage" * 100,
        beenToOtherEvents="Very long been to other events" * 100,
        communityContribution="Very long community contribution" * 100,
        notes="Very long notes" * 100,
    )

    assert response["data"]["updateGrant"]["__typename"] == "GrantErrors"
    assert response["data"]["updateGrant"]["errors"]["validationName"] == [
        "name: Cannot be more than 300 chars"
    ]
    assert response["data"]["updateGrant"]["errors"]["validationFullName"] == [
        "full_name: Cannot be more than 300 chars"
    ]
    assert response["data"]["updateGrant"]["errors"]["validationDepartureCountry"] == [
        "departure_country: Cannot be more than 100 chars"
    ]
    assert response["data"]["updateGrant"]["errors"]["validationNationality"] == [
        "nationality: Cannot be more than 100 chars"
    ]
    assert response["data"]["updateGrant"]["errors"]["validationDepartureCity"] == [
        "departure_city: Cannot be more than 100 chars"
    ]
    assert response["data"]["updateGrant"]["errors"]["validationWhy"] == [
        "why: Cannot be more than 1000 chars"
    ]
    assert response["data"]["updateGrant"]["errors"]["validationPythonUsage"] == [
        "python_usage: Cannot be more than 700 chars"
    ]
    assert response["data"]["updateGrant"]["errors"]["validationBeenToOtherEvents"] == [
        "been_to_other_events: Cannot be more than 500 chars"
    ]
    assert response["data"]["updateGrant"]["errors"][
        "validationCommunityContribution"
    ] == ["community_contribution: Cannot be more than 900 chars"]
    assert response["data"]["updateGrant"]["errors"]["validationNotes"] == [
        "notes: Cannot be more than 350 chars"
    ]


def test_cannot_update_grant_with_empty_values_if_needs_funds_for_travel(
    graphql_client,
    user,
):
    graphql_client.force_login(user)
    conference = ConferenceFactory(
        active_grants=True,
    )

    grant = GrantFactory(
        user_id=user.id,
        conference=conference,
    )

    response = _update_grant(
        graphql_client,
        grant=grant,
        needsFundsForTravel=True,
        departureCountry="",
        departureCity="",
        nationality="",
    )

    assert response["data"]["updateGrant"]["__typename"] == "GrantErrors"
    assert response["data"]["updateGrant"]["errors"]["validationDepartureCountry"] == [
        "departure_country: Cannot be empty"
    ]
    assert response["data"]["updateGrant"]["errors"]["validationDepartureCity"] == [
        "departure_city: Cannot be empty"
    ]
    assert response["data"]["updateGrant"]["errors"]["validationNationality"] == [
        "nationality: Cannot be empty"
    ]

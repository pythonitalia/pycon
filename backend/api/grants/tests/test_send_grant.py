import pytest

pytestmark = pytest.mark.django_db


def _send_grant(client, grant_factory, conference, **kwargs):
    grant = grant_factory.build(conference=conference)
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
                        validationOccupation: occupation
                        validationAgeGroup: ageGroup
                        validationPythonUsage: pythonUsage
                        validationBeenToOtherEvents: beenToOtherEvents
                        validationInterestedInVolunteering: interestedInVolunteering
                        validationNeedsFundsForTravel: needsFundsForTravel
                        validationWhy: why
                        validationNotes: notes
                        validationTravellingFrom: travellingFrom
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
        "beenToOtherEvents": grant.been_to_other_events,
        "interestedInVolunteering": grant.interested_in_volunteering,
        "needsFundsForTravel": grant.needs_funds_for_travel,
        "why": grant.why,
        "notes": grant.notes,
        "travellingFrom": grant.travelling_from,
    }

    variables = {**defaults, **kwargs}

    response = client.query(document, variables={"input": variables})

    return response


def test_send_grant(graphql_client, user, conference_factory, grant_factory):
    graphql_client.force_login(user)
    conference = conference_factory(active_grants=True)

    response = _send_grant(graphql_client, grant_factory, conference)

    assert response["data"]["sendGrant"]["__typename"] == "Grant"
    assert response["data"]["sendGrant"]["id"]


def test_cannot_send_a_grant_if_grants_are_closed(
    graphql_client, user, conference_factory, grant_factory
):
    graphql_client.force_login(user)
    conference = conference_factory(active_grants=False)

    response = _send_grant(graphql_client, grant_factory, conference)

    assert not response.get("errors")
    assert response["data"]["sendGrant"]["__typename"] == "GrantErrors"
    assert response["data"]["sendGrant"]["errors"]["nonFieldErrors"] == [
        "The grants form is not open!"
    ]


def test_cannot_send_a_grant_if_grants_deadline_do_not_exists(
    graphql_client, user, conference, grant_factory
):
    assert list(conference.deadlines.all()) == []
    graphql_client.force_login(user)

    response = _send_grant(graphql_client, grant_factory, conference)

    assert not response.get("errors")
    assert response["data"]["sendGrant"]["__typename"] == "GrantErrors"
    assert response["data"]["sendGrant"]["errors"]["nonFieldErrors"] == [
        "The grants form is not open!"
    ]


def test_cannot_send_a_grant_as_unlogged_user(
    graphql_client, conference, grant_factory
):
    resp = _send_grant(graphql_client, grant_factory, conference)

    assert resp["errors"][0]["message"] == "User not logged in"


def test_cannot_send_two_grants(
    graphql_client, user, grant_factory, conference_factory
):
    graphql_client.force_login(user)
    conference = conference_factory(active_grants=True)
    _send_grant(graphql_client, grant_factory, conference)

    response = _send_grant(graphql_client, grant_factory, conference)

    assert not response.get("errors")
    assert response["data"]["sendGrant"]["__typename"] == "GrantErrors"
    assert response["data"]["sendGrant"]["errors"]["nonFieldErrors"] == [
        "Grant already submitted!"
    ]


def test_invalid_conference(graphql_client, user, conference_factory, grant_factory):
    graphql_client.force_login(user)
    conference = conference_factory.build()

    response = _send_grant(graphql_client, grant_factory, conference)

    assert not response.get("errors")
    assert response["data"]["sendGrant"]["__typename"] == "GrantErrors"
    assert response["data"]["sendGrant"]["errors"]["validationConference"] == [
        "Invalid conference"
    ]


def test_cannot_send_grant_outside_allowed_values(
    graphql_client,
    user,
    conference_factory,
    grant_factory,
):
    graphql_client.force_login(user)
    conference = conference_factory(
        active_grants=True,
    )

    response = _send_grant(
        graphql_client,
        grant_factory,
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
    conference_factory,
    grant_factory,
):
    graphql_client.force_login(user)
    conference = conference_factory(
        active_grants=True,
    )

    response = _send_grant(
        graphql_client,
        grant_factory,
        conference,
        name="",
        fullName="",
        pythonUsage="",
        beenToOtherEvents="",
        why="",
    )

    assert response["data"]["sendGrant"]["__typename"] == "GrantErrors"
    assert response["data"]["sendGrant"]["errors"]["validationName"] == [
        "name: Cannot be empty"
    ]
    assert response["data"]["sendGrant"]["errors"]["validationFullName"] == [
        "full_name: Cannot be empty"
    ]

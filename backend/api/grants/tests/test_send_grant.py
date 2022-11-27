import pytest

pytestmark = pytest.mark.django_db


def _send_grant(client, grant_factory, conference, **kwargs):
    grant = grant_factory.build(conference=conference)
    document = """
        mutation SendGrantRequest($input: SendGrantRequestInput!) {
            sendGrantRequest(input: $input) {
                __typename

                ... on GrantRequest {
                    id
                }

                ... on SendGrantRequestErrors {
                    validationConference: conference
                    validationName: name
                    validationFullName: fullName
                    validationGender: gender
                    validationGrantType: grantType
                    validationOccupation: occupation
                    validationOccupation: occupation
                    validationAge: age
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
    """

    defaults = {
        "input": {
            "name": grant.name,
            "fullName": grant.full_name,
            "conference": grant.conference.code,
            "age": grant.age,
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
    }
    variables = {**defaults, **kwargs}

    response = client.query(document, variables=variables)

    return response


def test_send_grant(graphql_client, user, conference_factory, grant_factory):
    graphql_client.force_login(user)
    conference = conference_factory(active_grants=True)

    response = _send_grant(graphql_client, grant_factory, conference)

    assert response["data"]["sendGrantRequest"]["id"]


def test_cannot_send_a_grant_if_grants_are_closed(
    graphql_client, user, conference_factory, grant_factory
):
    graphql_client.force_login(user)
    conference = conference_factory(active_grants=False)

    response = _send_grant(graphql_client, grant_factory, conference)

    assert not response.get("errors")
    assert response["data"]["sendGrantRequest"]["nonFieldErrors"] == [
        "The grants form is now closed!"
    ]


def test_cannot_send_a_grant_if_grants_deadline_do_not_exists(
    graphql_client, user, conference, grant_factory
):
    assert list(conference.deadlines.all()) == []
    graphql_client.force_login(user)

    response = _send_grant(graphql_client, grant_factory, conference)

    assert not response.get("errors")
    assert response["data"]["sendGrantRequest"]["nonFieldErrors"] == [
        "The grants form is now closed!"
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

    assert response["data"]["sendGrantRequest"]["nonFieldErrors"] == [
        "Grant already submitted!"
    ]

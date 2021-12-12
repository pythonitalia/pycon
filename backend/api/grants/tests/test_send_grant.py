import pytest


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
                    validationEmail: email
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
            "email": grant.email,
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


@pytest.mark.django_db
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
        "The grants form is now " "closed!"
    ]

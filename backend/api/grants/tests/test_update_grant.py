from typing import Any, List, Optional

import pytest

pytestmark = pytest.mark.django_db


def snake_to_camel(value: str) -> str:
    return "".join(
        [
            word.capitalize() if index != 0 else word
            for index, word in enumerate(value.split("_"))
        ]
    )


def dict_to_camel(dict_: dict[str, Any]) -> dict[str, Any]:
    new = {}
    for k, v in dict_.items():
        if isinstance(k, dict):
            v = dict_to_camel(v)
        if isinstance(v, list):
            v = [dict_to_camel(item) if isinstance(item, dict) else item for item in v]

        new[snake_to_camel(k)] = v
    return new


def to_camel_dict(obj, exclude: Optional[List] = None) -> dict[str, Any]:
    if not exclude:
        exclude = []

    exclude.extend(["_state", "created", "modified", "to_camel_dict"])

    return dict_to_camel({k: v for k, v in obj.__dict__.items() if k not in exclude})


def _update_grant(graphql_client, grant, **kwargs):
    defaults = to_camel_dict(grant, exclude=["id", "user_id", "email", "conference_id"])

    query = """
    mutation updateGrant($input: UpdateGrantInput!){
        updateGrant(input: $input) {
            __typename

            ... on Grant {
                id
            }

            ... on GrantErrors {
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

    variables = {
        **defaults,
        **kwargs,
        "conference": grant.conference.code,
        "instance": grant.id,
    }

    response = graphql_client.query(query, variables={"input": variables})

    return response


def test_update_grant(graphql_client, user, conference_factory, grant_factory):
    graphql_client.force_login(user)
    conference = conference_factory(active_grants=True)
    grant = grant_factory(conference=conference, gender="female", user_id=user.id)

    response = _update_grant(
        graphql_client,
        grant,
        name="Marcotte",
        fullName="Marcotte B. A.",
        age=3,
        gender="male",
        occupation="student",
        grantType="diversity",
        pythonUsage="random",
        beenToOtherEvents="no",
        interestedInVolunteering="yes",
        needsFundsForTravel=True,
        why="why not",
        notes="🧸",
        travellingFrom="London",
    )

    grant.refresh_from_db()

    assert not response.get("errors")
    assert response["data"]["updateGrant"]["__typename"] == "Grant"


def test_cannot_update_a_grant_if_user_is_not_owner(
    graphql_client,
    user,
    user_factory,
    conference_factory,
    grant_factory,
):
    other_user = user_factory()
    conference = conference_factory(active_grants=True)
    grant = grant_factory(conference=conference, user_id=user.id)
    graphql_client.force_login(other_user)

    response = _update_grant(
        graphql_client,
        grant,
        name="Marcotte",
    )

    assert response["data"]["updateGrant"]["__typename"] == "GrantErrors"
    assert response["data"]["updateGrant"]["nonFieldErrors"] == [
        "You cannot edit this grant"
    ]


def test_cannot_update_a_grant_if_grants_are_closed(
    graphql_client, user, conference_factory, grant_factory
):
    graphql_client.force_login(user)
    conference = conference_factory(active_grants=False)
    grant = grant_factory(conference=conference, user_id=user.id)

    response = _update_grant(
        graphql_client,
        grant,
        name="Marcotte",
    )

    assert response["data"]["updateGrant"]["__typename"] == "GrantErrors"
    assert response["data"]["updateGrant"]["nonFieldErrors"] == [
        "The grants form is not open!"
    ]


def test_cannot_update_a_grant_if_grants_deadline_do_not_exists(
    graphql_client, user, grant_factory, conference
):
    assert list(conference.deadlines.all()) == []
    graphql_client.force_login(user)
    grant = grant_factory(conference=conference, user_id=user.id)

    response = _update_grant(graphql_client, grant)

    assert not response.get("errors")
    assert response["data"]["updateGrant"]["__typename"] == "GrantErrors"
    assert response["data"]["updateGrant"]["nonFieldErrors"] == [
        "The grants form is not open!"
    ]


def test_cannot_send_a_grant_as_unlogged_user(graphql_client, grant):
    resp = _update_grant(graphql_client, grant)

    assert resp["errors"][0]["message"] == "User not logged in"


def test_cannot_update_submission_with_lang_outside_allowed_values(
    graphql_client,
    user,
    conference_factory,
    grant_factory,
):
    graphql_client.force_login(user)
    conference = conference_factory(
        active_grants=True,
    )

    grant = grant_factory(
        user_id=user.id,
        conference=conference,
    )

    response = _update_grant(
        graphql_client,
        grant=grant,
        name="Marcotte" * 50,
        travellingFrom="Very long location" * 50,
    )

    assert response["data"]["updateGrant"]["__typename"] == "GrantErrors"
    assert response["data"]["updateGrant"]["validationName"] == [
        "name: Cannot be more than 300 chars"
    ]
    assert response["data"]["updateGrant"]["validationTravellingFrom"] == [
        "travelling_from: Cannot be more than 200 chars"
    ]

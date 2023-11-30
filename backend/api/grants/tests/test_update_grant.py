import pytest

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
        "conference": grant.conference.code,
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
        ageGroup="range_25_34",
        gender="male",
        occupation="student",
        grantType="diversity",
        pythonUsage="random",
        communityContribution="Soft toys meetups",
        beenToOtherEvents="no",
        interestedInVolunteering="yes",
        needsFundsForTravel=True,
        needVisa=True,
        needAccommodation=True,
        why="why not",
        notes="🧸",
        travellingFrom="London",
        website="https://marcotte.house",
        twitterHandle="@marcottebear",
        githubHandle="marcottebear",
        linkedinUrl="www.linkedin.com/in/marcotteba",
        mastodonHandle="marcottebear@marcotte.party",
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
    assert response["data"]["updateGrant"]["errors"]["nonFieldErrors"] == [
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
    assert response["data"]["updateGrant"]["errors"]["nonFieldErrors"] == [
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
    assert response["data"]["updateGrant"]["errors"]["nonFieldErrors"] == [
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
    assert response["data"]["updateGrant"]["errors"]["validationName"] == [
        "name: Cannot be more than 300 chars"
    ]
    assert response["data"]["updateGrant"]["errors"]["validationTravellingFrom"] == [
        "travelling_from: Cannot be more than 200 chars"
    ]

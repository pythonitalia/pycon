import datetime

import pytest


def _update_user(graphql_client, user, **kwargs):

    defaults = {
        "name": user.name,
        "full_name": user.full_name,
        "gender": user.gender,
        "open_to_recruiting": user.open_to_recruiting,
        "open_to_newsletter": user.open_to_newsletter,
        "date_birth": f"{user.date_birth:%Y-%m-%d}" if user.date_birth else "",
        "country": user.country if user.country else "",
    }
    variables = {**defaults, **kwargs}

    query = """
    mutation(
        $name: String,
        $full_name: String,
        $gender: String,
        $open_to_recruiting: Boolean!,
        $open_to_newsletter: Boolean!,
        $date_birth: String,
        $country: String
    ){
        update(input: {
            name: $name,
            fullName: $full_name,
            gender: $gender,
            openToRecruiting: $open_to_recruiting,
            openToNewsletter: $open_to_newsletter,
            dateBirth: $date_birth,
            country: $country
        }){
            __typename
            ... on MeUser {
                id
                name
                fullName
                gender
                openToRecruiting
                openToNewsletter
                dateBirth
                country
            }
            ... on UpdateErrors {
                validationName: name
                validationFullName: fullName
                validationGender: gender
                validationOpenToRecruiting: openToRecruiting
                validationOpenToNewsletter: openToNewsletter
                validationDateBirth: dateBirth
                validationCountry: country
                nonFieldErrors
            }
        }
    }
    """
    return (graphql_client.query(query=query, variables=variables), variables)


@pytest.mark.django_db
def test_update(graphql_client, user_factory):
    user = user_factory(
        name="John",
        full_name="John Lennon",
        gender="male",
        open_to_recruiting=True,
        open_to_newsletter=True,
        date_birth=datetime.datetime.strptime("1940-10-09", "%Y-%m-%d"),
        country="AT",
    )
    graphql_client.force_login(user)
    resp, variables = _update_user(graphql_client, user)

    assert resp["data"]["update"]["__typename"] == "MeUser"
    assert resp["data"]["update"]["id"] == str(user.id)
    assert resp["data"]["update"]["name"] == variables["name"]
    assert resp["data"]["update"]["fullName"] == variables["full_name"]
    assert resp["data"]["update"]["gender"] == variables["gender"]
    assert resp["data"]["update"]["openToRecruiting"] == variables["open_to_recruiting"]
    assert resp["data"]["update"]["openToNewsletter"] == variables["open_to_newsletter"]
    assert resp["data"]["update"]["dateBirth"] == variables["date_birth"]
    assert resp["data"]["update"]["country"] == variables["country"]


@pytest.mark.django_db
def test_update_multiple(graphql_client, user_factory):
    user = user_factory(
        name="John",
        full_name="John Lennon",
        gender="male",
        open_to_recruiting=True,
        open_to_newsletter=True,
        date_birth=datetime.datetime.strptime("1940-10-09", "%Y-%m-%d"),
        country="AT",
    )
    graphql_client.force_login(user)
    resp, variables = _update_user(graphql_client, user)

    user.name = "Aretha"
    user.full_name = "Aretha Franklin"
    user.gender = "female"
    user.open_to_newsletter = False
    user.open_to_recruiting = False
    user.date_birth = datetime.datetime.strptime("1942-03-25", "%Y-%m-%d")
    user.country = "US"
    resp, variables = _update_user(graphql_client, user)

    assert resp["data"]["update"]["__typename"] == "MeUser"
    assert resp["data"]["update"]["id"] == str(user.id)
    assert resp["data"]["update"]["name"] == variables["name"]
    assert resp["data"]["update"]["fullName"] == variables["full_name"]
    assert resp["data"]["update"]["gender"] == variables["gender"]
    assert resp["data"]["update"]["openToRecruiting"] == variables["open_to_recruiting"]
    assert resp["data"]["update"]["openToNewsletter"] == variables["open_to_newsletter"]
    assert resp["data"]["update"]["dateBirth"] == variables["date_birth"]
    assert resp["data"]["update"]["country"] == variables["country"]

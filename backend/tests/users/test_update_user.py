from pytest import mark

from users.models import User


def _update_user(graphql_client, user, **kwargs):
    defaults = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        # "gender": user.gender,
        # "date_birth": user.date_birth,
        # "business_name": user.business_name,
        # "fiscal_code": user.fiscal_code,
        # "vat_number": user.vat_number,
        # "phone_number": user.phone_number,
        # "recipient_code": user.recipient_code,
        # "pec_address": user.pec_address,
        # "address": user.address,
        # "country": user.country
    }
    variables = {**defaults, **kwargs}

    query = """
    mutation(
        $first_name: String,
        $last_name: String
    ){
        update(input: {
            firstName: $first_name,
            lastName: $last_name
        }){
            __typename
            ... on MeUserType {
                id
                firstName
                lastName
            }
            ... on UpdateErrors {
                nonFieldErrors
            }
        }
    }
    """
    return (graphql_client.query(query=query, variables=variables), variables)


@mark.django_db
def test_update(graphql_client, user_factory):
    user = user_factory(first_name="John", last_name="Lennon")
    graphql_client.force_login(user)
    resp, variables = _update_user(graphql_client, user)

    assert resp["data"]["update"]["__typename"] == "MeUserType"
    assert resp["data"]["update"]["id"] == str(variables["id"])
    assert resp["data"]["update"]["firstName"] == variables["first_name"]
    assert resp["data"]["update"]["lastName"] == variables["last_name"]


@mark.django_db
def test_update_not_authenticated_user_error(graphql_client):
    user, _ = User.objects.get_or_create(email="user@example.it", password="password")
    resp, variables = _update_user(graphql_client, user)

    assert resp["data"]["update"]["__typename"] == "UpdateErrors"
    assert resp["data"]["update"]["nonFieldErrors"] == [
        "Must authenticate to update User information"
    ]


@mark.django_db
def test_gender_a_caso():
    pass

from django.contrib.sessions.models import Session
from pytest import mark
from users.models import User


def _register_user(graphql_client, email, password):
    return graphql_client.query(
        """
    mutation($inputEmail: String!, $inputPassword: String!) {
        register(input: {email: $inputEmail, password: $inputPassword}) {
            __typename

            ... on RegisterErrors {
                email
                password
                nonFieldErrors
            }

            ... on MeUserType {
                id
            }
        }
    }
    """,
        variables={"inputEmail": email, "inputPassword": password},
    )


@mark.django_db
def test_register(graphql_client):
    response = _register_user(graphql_client, "test@user.it", "password")

    assert response["data"]["register"]["__typename"] == "MeUserType"

    user = User.objects.get(email="test@user.it")

    assert response["data"]["register"]["id"] == str(user.id)

    assert user.check_password("password")

    session = Session.objects.first()

    assert session.get_decoded()["_auth_user_id"] == str(user.id)


@mark.django_db
def test_cannot_register_if_the_email_is_already_used(graphql_client, user_factory):
    user_factory(email="marco@acierno.it")

    response = _register_user(graphql_client, "marco@acierno.it", "password")

    assert response["data"]["register"]["__typename"] == "RegisterErrors"
    assert response["data"]["register"]["email"] == [
        "This email is already used by another account"
    ]


@mark.django_db
def test_cannot_register_with_invalid_email(graphql_client):
    response = _register_user(graphql_client, "test", "password")

    assert response["data"]["register"]["__typename"] == "RegisterErrors"
    assert response["data"]["register"]["email"] == ["Enter a valid email address."]


@mark.django_db
def test_cannot_register_with_empty_email(graphql_client):
    response = _register_user(graphql_client, "", "password")

    assert response["data"]["register"]["__typename"] == "RegisterErrors"
    assert response["data"]["register"]["email"] == ["This field is required."]


@mark.django_db
def test_cannot_register_with_empty_password(graphql_client):
    response = _register_user(graphql_client, "marco@rollstudio.it", "")

    assert response["data"]["register"]["__typename"] == "RegisterErrors"
    assert response["data"]["register"]["password"] == ["This field is required."]

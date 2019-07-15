from pytest import mark

from django.contrib.sessions.models import Session


def _login_user(graphql_client, email, password):
    return graphql_client.query("""
    mutation($email: String!, $password: String!) {
        login(input: {email: $email, password: $password}) {
            __typename

            ... on MeUserType {
                id
                email
            }

            ... on EmailPasswordCombinationError {
                message
            }
        }
    }
    """,
        variables={
            'email': email,
            'password': password
        },
    )


@mark.django_db
def test_login_user(graphql_client, user_factory):
    user = user_factory(password='ciao')

    response = _login_user(
        graphql_client,
        user.email,
        'ciao',
    )

    assert response['data']['login']['__typename'] == 'MeUserType'

    assert response['data']['login']['id'] == str(user.id)
    assert response['data']['login']['email'] == user.email

    session = Session.objects.first()

    assert session.get_decoded()['_auth_user_id'] == str(user.id)


@mark.django_db
def test_cannot_login_with_the_wrong_password(graphql_client, user_factory):
    user = user_factory(password='ciao')

    response = _login_user(
        graphql_client,
        user.email,
        'hello',
    )

    assert response['data']['login']['__typename'] == 'EmailPasswordCombinationError'
    assert response['data']['login']['message'] == 'Wrong email/password combination'


@mark.django_db
def test_cannot_login_to_not_active_account(graphql_client, user_factory):
    user = user_factory(password='ciao', is_active=False)

    response = _login_user(
        graphql_client,
        user.email,
        'ciao',
    )

    assert response['data']['login']['__typename'] == 'EmailPasswordCombinationError'
    assert response['data']['login']['message'] == 'Wrong email/password combination'


@mark.django_db
def test_cannot_login_with_invalid_email(graphql_client, user_factory):
    user = user_factory(password='ciao', is_active=False)

    response = _login_user(
        graphql_client,
        'random@email.it',
        'ciao',
    )

    assert response['data']['login']['__typename'] == 'EmailPasswordCombinationError'
    assert response['data']['login']['message'] == 'Wrong email/password combination'

import pytest


@pytest.fixture()
def graphql_client(client):
    from .graphql_client import GraphQLClient

    return GraphQLClient(client)


@pytest.fixture()
def admin_graphql_client(client, admin_user):
    from .graphql_client import GraphQLClient

    client.force_login(admin_user)

    return GraphQLClient(client)

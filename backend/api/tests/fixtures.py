import pytest


@pytest.fixture()
def graphql_client(client):
    from .utils import GraphQLClient

    return GraphQLClient(client)

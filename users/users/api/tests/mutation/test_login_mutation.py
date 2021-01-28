from users.api.tests.graphql_client import graphql_client
from ward import test


@test("cannot login with non existent user")
def _(graphql_client=graphql_client):
    query = """
    mutation($input: LoginInput!) {
        login(input: $input) {
            __typename
        }
    }
    """
    response = graphql_client.query(
        query, variables={"input": {"email": "hah@pycon.it", "password": "ciao"}}
    )

    assert not response.errors
    assert response.data["login"]["__typename"] == "UsernameAndPasswordCombinationWrong"

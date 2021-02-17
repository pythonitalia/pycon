from association.api.tests.graphql_client import graphql_client
from association.tests.session import db
from ward import test


@test("ok")
async def _(graphql_client=graphql_client, db=db):
    query = """
    mutation($input: StripeCheckoutDataInput!) {
        setupStripeCheckout(requestData: $input) {
            __typename
        }
    }
    """
    response = await graphql_client.query(
        query, variables={"input": {"priceId": "price_1IJ6FUBdGh4ViRn9tkQFtU1R"}}
    )
    print(f"response : {response}")
    assert response.data["setupStripeCheckout"]["__typename"] == "StripeCheckoutCreated"

# from unittest.mock import patch

# from ward import test

# from api.tests.graphql_client import graphql_client
# from association.tests.session import db


# @test("Subscription created")
# async def _(graphql_client=graphql_client, db=db):
#     query = """
#     mutation {
#         subscribeUserToAssociation {
#             __typename
#             ... on CheckoutSession {
#                 __typename
#                 stripeSessionId
#             }
#         }
#     }
#     """
#     with patch(
#         "association.domain.services.subscribe_user_to_association",
#         return_value=StripeCheckoutSessionFactory.build(id="cs_test_12345"),
#     ) as service_mock:
#         response = await graphql_client.query(query, variables={})
#         assert (
#             response.data["subscribeUserToAssociation"]["__typename"]
#             == "CheckoutSession"
#         )
#         assert (
#             response.data["subscribeUserToAssociation"]["stripeSessionId"]
#             == "cs_test_12345"
#         )
#         service_mock.assert_called_once()

# from unittest.mock import patch

# from ward import test

# from api.tests.graphql_client import graphql_client
# from association.tests.session import db
# from association_membership.domain.exceptions import CustomerNotAvailable


# @test("Customer portal url returned")
# async def _(graphql_client=graphql_client, db=db):
#     query = """
#     mutation {
#         manageUserSubscription {
#             __typename
#             ... on CustomerPortalResponse {
#                 __typename
#                 billingPortalUrl
#             }
#         }
#     }
#     """
#     with patch(
#         "association.domain.services.manage_user_association_subscription",
#         return_value="https://stripe.com/stripe_test_customer_portal/cus_test_12345",
#     ) as service_mock:
#         response = await graphql_client.query(query, variables={})
#         assert (
#             response.data["manageUserSubscription"]["__typename"]
#             == "CustomerPortalResponse"
#         )
#         assert (
#             response.data["manageUserSubscription"]["billingPortalUrl"]
#             == "https://stripe.com/stripe_test_customer_portal/cus_test_12345"
#         )
#         service_mock.assert_called_once()


# @test("Customer Not Available")
# async def _(graphql_client=graphql_client, db=db):
#     query = """
#     mutation {
#         manageUserSubscription {
#             __typename
#             ... on CustomerNotAvailableError {
#                 __typename
#                 message
#             }
#         }
#     }
#     """
#     with patch(
#         "association.domain.services.manage_user_association_subscription",
#         return_value="https://stripe.com/stripe_test_customer_portal/cus_test_12345",
#     ) as service_mock:
#         service_mock.side_effect = CustomerNotAvailable()
#         response = await graphql_client.query(query, variables={})
#         assert (
#             response.data["manageUserSubscription"]["__typename"]
#             == "CustomerNotAvailableError"
#         )
#         assert (
#             response.data["manageUserSubscription"]["message"]
#             == "Customer not available"
#         )
#         assert not response.errors
#         service_mock.assert_called_once()

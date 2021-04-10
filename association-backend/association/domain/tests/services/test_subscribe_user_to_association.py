# import datetime

# import time_machine
# from ward import raises, test

# from association.domain import services
# from association.domain.entities.stripe import StripeCustomer, StripeSubscriptionStatus
# from association.domain.entities.subscriptions import SubscriptionState, UserData
# from association.domain.exceptions import (
#     AlreadySubscribed,
#     MultipleCustomerReturned,
#     MultipleCustomerSubscriptionsReturned,
# )
# from association.domain.tests.repositories.fake_repository import (
#     FakeAssociationRepository,
# )
# from association.tests.factories import (
#     StripeCustomerFactory,
#     StripeSubscriptionFactory,
#     SubscriptionFactory,
# )


# @test("No Subscription && No Customer -> return Checkout Session with new customer")
# async def _():
#     repository = FakeAssociationRepository(subscriptions=[])

#     checkout_session = await services.subscribe_user_to_association(
#         user_data=UserData(email="test_user@pycon.it", user_id=1357),
#         association_repository=repository,
#     )
#     assert checkout_session.customer_id != ""


# @test("No Subscription && No Customer -> creates Subscription with new Customer")
# async def _():
#     repository = FakeAssociationRepository(subscriptions=[])

#     with time_machine.travel("2021-03-13 13:00:00", tick=False):
#         checkout_session = await services.subscribe_user_to_association(
#             user_data=UserData(email="test_user@pycon.it", user_id=1357),
#             association_repository=repository,
#         )
#         subscription = await repository.get_subscription_by_user_id(1357)
#         assert subscription.state == SubscriptionState.PENDING
#         assert subscription.user_id == 1357
#         assert subscription.stripe_customer_id == checkout_session.customer_id
#         assert subscription.created_at == datetime.datetime(2021, 3, 13, 13, 0)


# @test(
#     "No Subscription && Existing Customer -> return Checkout Session with existing customer id"
# )
# async def _():
#     repository = FakeAssociationRepository(
#         subscriptions=[],
#         stripe_customers=[
#             StripeCustomerFactory.build(email="test_user@pycon.it", id="cus_test_12345")
#         ],
#     )

#     checkout_session = await services.subscribe_user_to_association(
#         user_data=UserData(email="test_user@pycon.it", user_id=1357),
#         association_repository=repository,
#     )
#     assert checkout_session.customer_id == "cus_test_12345"


# @test(
#     "No Subscription && Existing Customer -> creates Subscription with existing customer_id"
# )
# async def _():
#     repository = FakeAssociationRepository(
#         subscriptions=[],
#         stripe_customers=[
#             StripeCustomerFactory.build(email="test_user@pycon.it", id="cus_test_12345")
#         ],
#     )

#     with time_machine.travel("2021-03-13 13:00:00", tick=False):
#         checkout_session = await services.subscribe_user_to_association(
#             user_data=UserData(email="test_user@pycon.it", user_id=1357),
#             association_repository=repository,
#         )
#         subscription = await repository.get_subscription_by_user_id(1357)
#         assert subscription.state == SubscriptionState.PENDING
#         assert subscription.user_id == 1357
#         assert subscription.stripe_customer_id == "cus_test_12345"
#         assert subscription.stripe_customer_id == checkout_session.customer_id
#         assert subscription.created_at == datetime.datetime(2021, 3, 13, 13, 0)


# @test(
#     "No Subscription && 2 Existing Customers with same email -> raises MultipleCustomerReturned"
# )
# async def _():
#     repository = FakeAssociationRepository(
#         subscriptions=[],
#         stripe_customers=[
#             StripeCustomer(id="cus_test_12345", email="old_stripe_customer@pycon.it"),
#             StripeCustomer(id="cus_test_12346", email="old_stripe_customer@pycon.it"),
#         ],
#     )
#     with raises(MultipleCustomerReturned):
#         await services.subscribe_user_to_association(
#             user_data=UserData(email="old_stripe_customer@pycon.it", user_id=1357),
#             association_repository=repository,
#         )


# @test(
#     "subscription PENDING && stripe_customer_id && NO stripe_subscription -> returns new checkout session with old customer_id"
# )
# async def _():
#     orig_subscription = SubscriptionFactory(
#         user_id=1357,
#         state=SubscriptionState.PENDING,
#         stripe_customer_id="cus_test_12347",
#     )
#     # assert orig_subscription.stripe_subscription_id != ""

#     repository = FakeAssociationRepository(
#         subscriptions=[orig_subscription], stripe_subscriptions=[]
#     )

#     checkout_session = await services.subscribe_user_to_association(
#         user_data=UserData(email="test_user@pycon.it", user_id=1357),
#         association_repository=repository,
#     )
#     assert checkout_session.customer_id == orig_subscription.stripe_customer_id
#     assert checkout_session.customer_id == "cus_test_12347"


# @test(
#     "subscription PENDING && stripe_customer_id && NO stripe_subscription -> updates subscription"
# )
# async def _():
#     orig_subscription = SubscriptionFactory(
#         user_id=1357,
#         state=SubscriptionState.PENDING,
#         stripe_customer_id="cus_test_12347",
#     )

#     repository = FakeAssociationRepository(
#         subscriptions=[orig_subscription], stripe_subscriptions=[]
#     )

#     with time_machine.travel("2021-03-13 13:00:00", tick=False):
#         await services.subscribe_user_to_association(
#             user_data=UserData(email="test_user@pycon.it", user_id=1357),
#             association_repository=repository,
#         )
#         subscription = await repository.get_subscription_by_user_id(1357)
#         assert subscription.state == SubscriptionState.PENDING
#         assert subscription.user_id == 1357
#         assert subscription.stripe_customer_id == orig_subscription.stripe_customer_id
#         assert subscription.stripe_customer_id == "cus_test_12347"
#         assert subscription.modified_at == datetime.datetime(2021, 3, 13, 13, 0)


# @test(
#     "subscription PENDING && stripe_customer_id && 2 ACTIVE stripe_subscriptions with same stripe_customer_id -> MultipleCustomerSubscriptionsReturned"
# )
# async def _():
#     orig_subscription = SubscriptionFactory(
#         user_id=1357,
#         state=SubscriptionState.PENDING,
#         stripe_customer_id="cus_test_12347",
#     )
#     # assert orig_subscription.stripe_subscription_id != ""

#     repository = FakeAssociationRepository(
#         subscriptions=[orig_subscription],
#         stripe_subscriptions=[
#             StripeSubscriptionFactory.build(
#                 customer_id=orig_subscription.stripe_customer_id,
#                 status=StripeSubscriptionStatus.ACTIVE,
#             ),
#             StripeSubscriptionFactory.build(
#                 customer_id=orig_subscription.stripe_customer_id,
#                 status=StripeSubscriptionStatus.ACTIVE,
#             ),
#         ],
#     )
#     with raises(MultipleCustomerSubscriptionsReturned):
#         await services.subscribe_user_to_association(
#             user_data=UserData(email="test_user@pycon.it", user_id=1357),
#             association_repository=repository,
#         )


# @test(
#     "subscription PENDING && stripe_customer_id && 2 stripe_subscriptions, but 1 canceled, with same stripe_customer_id -> No MultipleCustomerSubscriptionsReturned raised",
#     tags=["failing"],
# )
# async def _():
#     orig_subscription = SubscriptionFactory(
#         user_id=1357,
#         state=SubscriptionState.PENDING,
#         stripe_customer_id="cus_test_12347",
#     )
#     # assert orig_subscription.stripe_subscription_id != ""

#     repository = FakeAssociationRepository(
#         subscriptions=[orig_subscription],
#         stripe_subscriptions=[
#             StripeSubscriptionFactory.build(
#                 customer_id=orig_subscription.stripe_customer_id,
#                 status=StripeSubscriptionStatus.INCOMPLETE,
#             ),
#             StripeSubscriptionFactory.build(
#                 customer_id=orig_subscription.stripe_customer_id,
#                 status=StripeSubscriptionStatus.CANCELED,
#             ),
#         ],
#     )
#     checkout_session = await services.subscribe_user_to_association(
#         user_data=UserData(email="test_user@pycon.it", user_id=1357),
#         association_repository=repository,
#     )
#     assert checkout_session.customer_id == orig_subscription.stripe_customer_id
#     assert checkout_session.customer_id == "cus_test_12347"


# @test(
#     "subscription PENDING && stripe_customer_id && stripe_subscription -> updates subscription"
# )
# async def _():
#     orig_subscription = SubscriptionFactory(
#         user_id=1357,
#         state=SubscriptionState.PENDING,
#         stripe_customer_id="cus_test_12347",
#     )

#     repository = FakeAssociationRepository(
#         subscriptions=[orig_subscription], stripe_subscriptions=[]
#     )

#     with time_machine.travel("2021-03-13 13:00:00", tick=False):
#         await services.subscribe_user_to_association(
#             user_data=UserData(email="test_user@pycon.it", user_id=1357),
#             association_repository=repository,
#         )
#         subscription = await repository.get_subscription_by_user_id(1357)
#         assert subscription.state == SubscriptionState.PENDING
#         assert subscription.user_id == 1357
#         assert subscription.stripe_customer_id == orig_subscription.stripe_customer_id
#         assert subscription.stripe_customer_id == "cus_test_12347"
#         assert subscription.modified_at == datetime.datetime(2021, 3, 13, 13, 0)


# @test(
#     "subscription PENDING && NO stripe_customer_id && NO stripe_subscription -> returns new checkout session with new customer_id"
# )
# async def _():
#     orig_subscription = SubscriptionFactory(
#         user_id=1357, state=SubscriptionState.PENDING, stripe_customer_id=""
#     )
#     old_stripe_customer_id = orig_subscription.stripe_customer_id
#     assert old_stripe_customer_id == ""

#     repository = FakeAssociationRepository(
#         subscriptions=[orig_subscription], stripe_subscriptions=[]
#     )

#     checkout_session = await services.subscribe_user_to_association(
#         user_data=UserData(email="test_user@pycon.it", user_id=1357),
#         association_repository=repository,
#     )
#     assert checkout_session.customer_id != old_stripe_customer_id


# @test(
#     "subscription PENDING && NO stripe_customer_id && NO stripe_subscription -> updates subscription with new customer_id"
# )
# async def _():
#     orig_subscription = SubscriptionFactory(
#         user_id=1357, state=SubscriptionState.PENDING, stripe_customer_id=""
#     )
#     old_stripe_customer_id = orig_subscription.stripe_customer_id
#     assert old_stripe_customer_id == ""

#     repository = FakeAssociationRepository(
#         subscriptions=[orig_subscription], stripe_subscriptions=[]
#     )

#     with time_machine.travel("2021-03-13 13:00:00", tick=False):
#         checkout_session = await services.subscribe_user_to_association(
#             user_data=UserData(email="test_user@pycon.it", user_id=1357),
#             association_repository=repository,
#         )
#         subscription = await repository.get_subscription_by_user_id(1357)
#         assert subscription.state == SubscriptionState.PENDING
#         assert subscription.user_id == 1357
#         assert subscription.stripe_customer_id != old_stripe_customer_id
#         assert subscription.stripe_customer_id == checkout_session.customer_id
#         assert subscription.modified_at == datetime.datetime(2021, 3, 13, 13, 0)


# @test("subscription ACTIVE -> raises AlreadySubscribed")
# async def _():
#     repository = FakeAssociationRepository(
#         subscriptions=[
#             SubscriptionFactory(user_id=1357, state=SubscriptionState.ACTIVE)
#         ],
#     )
#     with raises(AlreadySubscribed):
#         await services.subscribe_user_to_association(
#             user_data=UserData(email="test_user@pycon.it", user_id=1357),
#             association_repository=repository,
#         )


# @test("subscription EXPIRED -> raises AlreadySubscribed")
# async def _():
#     repository = FakeAssociationRepository(
#         subscriptions=[
#             SubscriptionFactory(user_id=1357, state=SubscriptionState.EXPIRED)
#         ],
#     )
#     with raises(AlreadySubscribed):
#         await services.subscribe_user_to_association(
#             user_data=UserData(email="test_user@pycon.it", user_id=1357),
#             association_repository=repository,
#         )


# @test(
#     "subscription CANCELED && stripe_customer_id -> returns new checkout session with old customer_id"
# )
# async def _():
#     orig_subscription = SubscriptionFactory(
#         user_id=1357,
#         state=SubscriptionState.CANCELED,
#         stripe_customer_id="cus_test_12347",
#     )
#     # assert orig_subscription.stripe_subscription_id != ""

#     repository = FakeAssociationRepository(
#         subscriptions=[orig_subscription], stripe_subscriptions=[]
#     )

#     checkout_session = await services.subscribe_user_to_association(
#         user_data=UserData(email="test_user@pycon.it", user_id=1357),
#         association_repository=repository,
#     )
#     assert checkout_session.customer_id == orig_subscription.stripe_customer_id
#     assert checkout_session.customer_id == "cus_test_12347"


# @test(
#     "subscription CANCELED && stripe_customer_id -> updates subscription with state PENDING"
# )
# async def _():
#     orig_subscription = SubscriptionFactory(
#         user_id=1357,
#         state=SubscriptionState.CANCELED,
#         stripe_customer_id="cus_test_12347",
#     )

#     repository = FakeAssociationRepository(
#         subscriptions=[orig_subscription], stripe_subscriptions=[]
#     )

#     with time_machine.travel("2021-03-13 13:00:00", tick=False):
#         await services.subscribe_user_to_association(
#             user_data=UserData(email="test_user@pycon.it", user_id=1357),
#             association_repository=repository,
#         )
#         subscription = await repository.get_subscription_by_user_id(1357)
#         assert subscription.state == SubscriptionState.PENDING
#         assert subscription.user_id == 1357
#         assert subscription.stripe_customer_id == orig_subscription.stripe_customer_id
#         assert subscription.stripe_customer_id == "cus_test_12347"
#         assert subscription.modified_at == datetime.datetime(2021, 3, 13, 13, 0)


# @test(
#     "subscription CANCELED && NO stripe_customer_id -> returns new checkout session with new customer_id"
# )
# async def _():
#     orig_subscription = SubscriptionFactory(
#         user_id=1357, state=SubscriptionState.CANCELED, stripe_customer_id=""
#     )
#     old_stripe_customer_id = orig_subscription.stripe_customer_id
#     assert old_stripe_customer_id == ""

#     repository = FakeAssociationRepository(
#         subscriptions=[orig_subscription], stripe_subscriptions=[]
#     )

#     checkout_session = await services.subscribe_user_to_association(
#         user_data=UserData(email="test_user@pycon.it", user_id=1357),
#         association_repository=repository,
#     )
#     assert checkout_session.customer_id != old_stripe_customer_id


# @test(
#     "subscription CANCELED && NO stripe_customer_id -> updates subscription with state PENDING && new customer_id"
# )
# async def _():
#     orig_subscription = SubscriptionFactory(
#         user_id=1357, state=SubscriptionState.CANCELED, stripe_customer_id=""
#     )
#     old_stripe_customer_id = orig_subscription.stripe_customer_id
#     assert old_stripe_customer_id == ""

#     repository = FakeAssociationRepository(
#         subscriptions=[orig_subscription], stripe_subscriptions=[]
#     )

#     with time_machine.travel("2021-03-13 13:00:00", tick=False):
#         checkout_session = await services.subscribe_user_to_association(
#             user_data=UserData(email="test_user@pycon.it", user_id=1357),
#             association_repository=repository,
#         )
#         subscription = await repository.get_subscription_by_user_id(1357)
#         assert subscription.state == SubscriptionState.PENDING
#         assert subscription.user_id == 1357
#         assert subscription.stripe_customer_id != old_stripe_customer_id
#         assert subscription.stripe_customer_id == checkout_session.customer_id
#         assert subscription.modified_at == datetime.datetime(2021, 3, 13, 13, 0)

# from ward import raises, test

# from association.domain import services
# from association.domain.entities.stripe import StripeSubscriptionStatus
# from association.domain.entities.subscriptions import SubscriptionState
# from association.domain.exceptions import (
#     InconsistentStateTransitionError,
#     SubscriptionNotFound,
# )
# from association.domain.tests.repositories.fake_repository import (
#     FakeAssociationRepository,
# )
# from association.tests.factories import (
#     StripeSubscriptionFactory,
#     SubscriptionFactory,
#     SubscriptionPaymentFactory,
# )


# @test("Subscription updated ACTIVE")
# async def _():
#     sut_subscription = SubscriptionFactory(
#         stripe_subscription_id="sub_test_1234", state=SubscriptionState.EXPIRED
#     )
#     assert sut_subscription.stripe_subscription_id == "sub_test_1234"
#     assert sut_subscription.state == SubscriptionState.EXPIRED

#     repository = FakeAssociationRepository(subscriptions=[sut_subscription])

#     subscription = await services.update_subscription_from_external_subscription(
#         stripe_subscription=StripeSubscriptionFactory.build(
#             id=sut_subscription.stripe_subscription_id,
#             status=StripeSubscriptionStatus.ACTIVE,
#         ),
#         association_repository=repository,
#     )

#     assert (
#         subscription.stripe_subscription_id == sut_subscription.stripe_subscription_id
#     )
#     assert subscription.state == SubscriptionState.ACTIVE


# @test("SubscriptionNotFound raised")
# async def _():
#     repository = FakeAssociationRepository(subscriptions=[])

#     with raises(SubscriptionNotFound):
#         await services.update_subscription_from_external_subscription(
#             stripe_subscription=StripeSubscriptionFactory.build(
#                 id=SubscriptionFactory.build().stripe_subscription_id,
#                 status=StripeSubscriptionStatus.ACTIVE,
#             ),
#             association_repository=repository,
#         )


# @test("Subscription update does not raise if status changes")
# async def _():
#     sut_subscription = SubscriptionFactory(
#         stripe_subscription_id="sub_test_1234", state=SubscriptionState.ACTIVE
#     )
#     assert sut_subscription.stripe_subscription_id == "sub_test_1234"
#     assert sut_subscription.state == SubscriptionState.ACTIVE

#     repository = FakeAssociationRepository(subscriptions=[sut_subscription])

#     subscription = await services.update_subscription_from_external_subscription(
#         stripe_subscription=StripeSubscriptionFactory.build(
#             id=sut_subscription.stripe_subscription_id,
#             status=StripeSubscriptionStatus.ACTIVE,
#         ),
#         association_repository=repository,
#     )

#     assert (
#         subscription.stripe_subscription_id == sut_subscription.stripe_subscription_id
#     )
#     assert subscription.state == SubscriptionState.ACTIVE


# @test("Subscription update ACTIVE")
# async def _():
#     sut_subscription = SubscriptionFactory()
#     repository = FakeAssociationRepository(subscriptions=[sut_subscription])

#     subscription = await services.update_subscription_from_external_subscription(
#         stripe_subscription=StripeSubscriptionFactory.build(
#             id=sut_subscription.stripe_subscription_id,
#             status=StripeSubscriptionStatus.ACTIVE,
#         ),
#         association_repository=repository,
#     )

#     assert subscription.state == SubscriptionState.ACTIVE


# @test("Subscription update INCOMPLETE -> PENDING")
# async def _():
#     sut_subscription = SubscriptionFactory()
#     repository = FakeAssociationRepository(subscriptions=[sut_subscription])

#     subscription = await services.update_subscription_from_external_subscription(
#         stripe_subscription=StripeSubscriptionFactory.build(
#             id=sut_subscription.stripe_subscription_id,
#             status=StripeSubscriptionStatus.INCOMPLETE,
#         ),
#         association_repository=repository,
#     )

#     assert subscription.state == SubscriptionState.PENDING


# @test("Subscription update INCOMPLETE_EXPIRED -> PENDING + Deleted subscription_id")
# async def _():
#     sut_subscription = SubscriptionFactory(state=SubscriptionState.PENDING)
#     repository = FakeAssociationRepository(subscriptions=[sut_subscription])

#     assert sut_subscription.stripe_subscription_id != ""

#     subscription = await services.update_subscription_from_external_subscription(
#         stripe_subscription=StripeSubscriptionFactory.build(
#             id=sut_subscription.stripe_subscription_id,
#             status=StripeSubscriptionStatus.INCOMPLETE_EXPIRED,
#         ),
#         association_repository=repository,
#     )

#     assert subscription.state == SubscriptionState.PENDING
#     assert subscription.stripe_subscription_id == ""


# @test(
#     "Subscription update INCOMPLETE_EXPIRED -> raise InconsistentStateTransitionError if subscription state is ACTIVE"
# )
# async def _():
#     sut_subscription = SubscriptionFactory(state=SubscriptionState.ACTIVE)
#     repository = FakeAssociationRepository(subscriptions=[sut_subscription])

#     with raises(InconsistentStateTransitionError):
#         await services.update_subscription_from_external_subscription(
#             stripe_subscription=StripeSubscriptionFactory.build(
#                 id=sut_subscription.stripe_subscription_id,
#                 status=StripeSubscriptionStatus.INCOMPLETE_EXPIRED,
#             ),
#             association_repository=repository,
#         )


# @test(
#     "Subscription update INCOMPLETE_EXPIRED -> raise InconsistentStateTransitionError if subscription state is EXPIRED"
# )
# async def _():
#     sut_subscription = SubscriptionFactory(state=SubscriptionState.EXPIRED)
#     repository = FakeAssociationRepository(subscriptions=[sut_subscription])

#     with raises(InconsistentStateTransitionError):
#         await services.update_subscription_from_external_subscription(
#             stripe_subscription=StripeSubscriptionFactory.build(
#                 id=sut_subscription.stripe_subscription_id,
#                 status=StripeSubscriptionStatus.INCOMPLETE_EXPIRED,
#             ),
#             association_repository=repository,
#         )


# @test(
#     "Subscription update INCOMPLETE_EXPIRED -> raise InconsistentStateTransitionError if subscription has associated Payments"
# )
# async def _():
#     sut_subscription = SubscriptionFactory(state=SubscriptionState.PENDING)
#     subscription_payment = SubscriptionPaymentFactory(subscription=sut_subscription)
#     repository = FakeAssociationRepository(
#         subscriptions=[sut_subscription],
#         subscription_payments=[subscription_payment],
#     )

#     with raises(InconsistentStateTransitionError):
#         await services.update_subscription_from_external_subscription(
#             stripe_subscription=StripeSubscriptionFactory.build(
#                 id=sut_subscription.stripe_subscription_id,
#                 status=StripeSubscriptionStatus.INCOMPLETE_EXPIRED,
#             ),
#             association_repository=repository,
#         )


# @test("Subscription update CANCELED -> CANCELED + Deleted session_id & subscription_id")
# async def _():
#     sut_subscription = SubscriptionFactory(state=SubscriptionState.ACTIVE)
#     repository = FakeAssociationRepository(subscriptions=[sut_subscription])

#     assert sut_subscription.stripe_subscription_id != ""

#     subscription = await services.update_subscription_from_external_subscription(
#         stripe_subscription=StripeSubscriptionFactory.build(
#             id=sut_subscription.stripe_subscription_id,
#             status=StripeSubscriptionStatus.CANCELED,
#         ),
#         association_repository=repository,
#     )

#     assert subscription.state == SubscriptionState.CANCELED
#     assert subscription.stripe_subscription_id == ""


# @test("Subscription update UNPAID -> CANCELED + Deleted session_id & subscription_id")
# async def _():
#     sut_subscription = SubscriptionFactory(state=SubscriptionState.ACTIVE)
#     repository = FakeAssociationRepository(subscriptions=[sut_subscription])

#     assert sut_subscription.stripe_subscription_id != ""

#     subscription = await services.update_subscription_from_external_subscription(
#         stripe_subscription=StripeSubscriptionFactory.build(
#             id=sut_subscription.stripe_subscription_id,
#             status=StripeSubscriptionStatus.UNPAID,
#         ),
#         association_repository=repository,
#     )

#     assert subscription.state == SubscriptionState.CANCELED
#     assert subscription.stripe_subscription_id == ""


# @test("Subscription update PAST_DUE -> EXPIRED")
# async def _():
#     sut_subscription = SubscriptionFactory()
#     repository = FakeAssociationRepository(subscriptions=[sut_subscription])

#     subscription = await services.update_subscription_from_external_subscription(
#         stripe_subscription=StripeSubscriptionFactory.build(
#             id=sut_subscription.stripe_subscription_id,
#             status=StripeSubscriptionStatus.PAST_DUE,
#         ),
#         association_repository=repository,
#     )

#     assert subscription.state == SubscriptionState.EXPIRED

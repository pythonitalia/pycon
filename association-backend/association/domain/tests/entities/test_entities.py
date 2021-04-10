# from ward import raises, test

# from association.domain.entities.stripe import StripeSubscriptionStatus
# from association.domain.entities.subscriptions import SubscriptionState
# from association.domain.exceptions import InconsistentStateTransitionError
# from association.tests.factories import (
#     StripeSubscriptionFactory,
#     SubscriptionFactory,
#     SubscriptionPaymentFactory,
# )


# @test("Subscription updated ACTIVE")
# async def _():
#     subscription = SubscriptionFactory(state=SubscriptionState.EXPIRED)
#     stripe_subscription = StripeSubscriptionFactory.build(
#         id=subscription.stripe_subscription_id, status=StripeSubscriptionStatus.ACTIVE
#     )
#     assert subscription.state == SubscriptionState.EXPIRED
#     subscription = subscription.sync_with_stripe_subscription(stripe_subscription)
#     assert subscription.state == SubscriptionState.ACTIVE


# @test("Subscription update does not raise if status doen't change")
# async def _():
#     subscription = SubscriptionFactory(state=SubscriptionState.EXPIRED)
#     stripe_subscription = StripeSubscriptionFactory.build(
#         id=subscription.stripe_subscription_id, status=StripeSubscriptionStatus.PAST_DUE
#     )
#     assert subscription.state == SubscriptionState.EXPIRED
#     subscription = subscription.sync_with_stripe_subscription(stripe_subscription)
#     assert subscription.state == SubscriptionState.EXPIRED


# @test("Subscription update ACTIVE")
# async def _():
#     subscription = SubscriptionFactory(state=SubscriptionState.EXPIRED)
#     stripe_subscription = StripeSubscriptionFactory.build(
#         id=subscription.stripe_subscription_id, status=StripeSubscriptionStatus.ACTIVE
#     )
#     assert subscription.state == SubscriptionState.EXPIRED
#     subscription = subscription.sync_with_stripe_subscription(stripe_subscription)
#     assert subscription.state == SubscriptionState.ACTIVE


# @test("Subscription update INCOMPLETE -> PENDING")
# async def _():
#     subscription = SubscriptionFactory()
#     stripe_subscription = StripeSubscriptionFactory.build(
#         id=subscription.stripe_subscription_id,
#         status=StripeSubscriptionStatus.INCOMPLETE,
#     )
#     subscription = subscription.sync_with_stripe_subscription(stripe_subscription)
#     assert subscription.state == SubscriptionState.PENDING


# @test("Subscription update INCOMPLETE_EXPIRED -> PENDING + Deleted subscription_id")
# async def _():
#     subscription = SubscriptionFactory(state=SubscriptionState.PENDING)
#     stripe_subscription = StripeSubscriptionFactory.build(
#         id=subscription.stripe_subscription_id,
#         status=StripeSubscriptionStatus.INCOMPLETE_EXPIRED,
#     )
#     subscription = subscription.sync_with_stripe_subscription(stripe_subscription)
#     assert subscription.state == SubscriptionState.PENDING


# @test(
#     "Subscription update INCOMPLETE_EXPIRED -> raise InconsistentStateTransitionError if subscription state is ACTIVE"
# )
# async def _():
#     subscription = SubscriptionFactory(state=SubscriptionState.ACTIVE)
#     stripe_subscription = StripeSubscriptionFactory.build(
#         id=subscription.stripe_subscription_id,
#         status=StripeSubscriptionStatus.INCOMPLETE_EXPIRED,
#     )
#     with raises(InconsistentStateTransitionError):
#         subscription.sync_with_stripe_subscription(stripe_subscription)


# @test(
#     "Subscription update INCOMPLETE_EXPIRED -> raise InconsistentStateTransitionError if subscription state is EXPIRED"
# )
# async def _():
#     subscription = SubscriptionFactory(state=SubscriptionState.EXPIRED)
#     stripe_subscription = StripeSubscriptionFactory.build(
#         id=subscription.stripe_subscription_id,
#         status=StripeSubscriptionStatus.INCOMPLETE_EXPIRED,
#     )
#     with raises(InconsistentStateTransitionError):
#         subscription.sync_with_stripe_subscription(stripe_subscription)


# @test(
#     "Subscription update INCOMPLETE_EXPIRED -> raise InconsistentStateTransitionError if subscription has associated Payments"
# )
# async def _():
#     subscription = SubscriptionFactory(state=SubscriptionState.PENDING)
#     SubscriptionPaymentFactory(subscription=subscription)
#     stripe_subscription = StripeSubscriptionFactory.build(
#         id=subscription.stripe_subscription_id,
#         status=StripeSubscriptionStatus.INCOMPLETE_EXPIRED,
#     )
#     with raises(InconsistentStateTransitionError):
#         subscription.sync_with_stripe_subscription(stripe_subscription)


# @test("Subscription update CANCELED -> CANCELED + Deleted session_id & subscription_id")
# async def _():
#     subscription = SubscriptionFactory(state=SubscriptionState.ACTIVE)
#     stripe_subscription = StripeSubscriptionFactory.build(
#         id=subscription.stripe_subscription_id, status=StripeSubscriptionStatus.CANCELED
#     )
#     subscription = subscription.sync_with_stripe_subscription(stripe_subscription)
#     assert subscription.state == SubscriptionState.CANCELED
#     assert subscription.stripe_subscription_id == ""


# @test("Subscription update UNPAID -> CANCELED + Deleted subscription_id")
# async def _():
#     subscription = SubscriptionFactory(state=SubscriptionState.ACTIVE)
#     stripe_subscription = StripeSubscriptionFactory.build(
#         id=subscription.stripe_subscription_id, status=StripeSubscriptionStatus.UNPAID
#     )
#     subscription = subscription.sync_with_stripe_subscription(stripe_subscription)
#     assert subscription.state == SubscriptionState.CANCELED
#     assert subscription.stripe_subscription_id == ""


# @test("Subscription update PAST_DUE -> EXPIRED")
# async def _():
#     subscription = SubscriptionFactory(state=SubscriptionState.ACTIVE)
#     stripe_subscription = StripeSubscriptionFactory.build(
#         id=subscription.stripe_subscription_id, status=StripeSubscriptionStatus.PAST_DUE
#     )
#     subscription = subscription.sync_with_stripe_subscription(stripe_subscription)
#     assert subscription.state == SubscriptionState.EXPIRED

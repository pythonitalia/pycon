import datetime
from typing import cast

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select
from ward import test

from association.domain.entities.subscription_entities import (
    Subscription,
    SubscriptionState,
)
from association.domain.repositories import AssociationRepository
from association.tests.factories import subscription_factory
from association.tests.session import cleanup_db, db, second_session


@test("save_subscription")
async def _(db=db, second_session=second_session, cleanup_db=cleanup_db):
    db = cast(AsyncSession, db)
    second_session = cast(AsyncSession, second_session)

    repository = AssociationRepository(db)

    await repository.save_subscription(
        Subscription(
            user_id=1234,
            creation_date=datetime.datetime(
                2020, 1, 1, 1, 0, tzinfo=datetime.timezone.utc
            ),
            stripe_session_id="cs_test_a1wtX1HXf3iOjdQK1cyEN3YavPmxSaTkdfo2fCAPLqlOPT3blEZrUOIlaQ",
            state=SubscriptionState.PENDING,
            stripe_id="sub_test_IxcENZqOBlHAJo",
            stripe_customer_id="cus_test_IuwfUVsdQFNvqc",
        )
    )
    await repository.commit()

    query = select(Subscription).where(Subscription.user_id == 1234)
    db_subscription: Subscription = (await second_session.execute(query)).scalar()

    assert db_subscription
    assert db_subscription.user_id == 1234
    assert db_subscription.creation_date == datetime.datetime(
        2020, 1, 1, 1, 0, tzinfo=datetime.timezone.utc
    )
    assert (
        db_subscription.stripe_session_id
        == "cs_test_a1wtX1HXf3iOjdQK1cyEN3YavPmxSaTkdfo2fCAPLqlOPT3blEZrUOIlaQ"
    )
    assert db_subscription.state == SubscriptionState.PENDING
    assert db_subscription.stripe_id == "sub_test_IxcENZqOBlHAJo"
    assert db_subscription.stripe_customer_id == "cus_test_IuwfUVsdQFNvqc"


@test("get subscription by user_id")
async def _(
    db=db,
    second_session=second_session,
    subscription_factory=subscription_factory,
    cleanup_db=cleanup_db,
):
    db = cast(AsyncSession, db)
    second_session = cast(AsyncSession, second_session)

    await subscription_factory(user_id=12345)
    await db.commit()

    repository = AssociationRepository(db)
    found_subscription = await repository.get_subscription_by_user_id(12345)

    query = select(Subscription).where(Subscription.user_id == 12345)
    raw_query_subscription: Subscription = (
        await second_session.execute(query)
    ).scalar()

    # Check what we get executing the "raw query"
    # and what the repository returned. Is this the same thing?
    assert found_subscription.user_id == raw_query_subscription.user_id
    assert found_subscription.creation_date == raw_query_subscription.creation_date
    assert (
        found_subscription.stripe_session_id == raw_query_subscription.stripe_session_id
    )
    assert found_subscription.state == raw_query_subscription.state
    assert found_subscription.stripe_id == raw_query_subscription.stripe_id
    assert (
        found_subscription.stripe_customer_id
        == raw_query_subscription.stripe_customer_id
    )


@test("get subscription by user_email")
async def _(
    db=db,
    second_session=second_session,
    subscription_factory=subscription_factory,
    cleanup_db=cleanup_db,
):
    db = cast(AsyncSession, db)
    second_session = cast(AsyncSession, second_session)

    await subscription_factory(user_email="user_12345@pycon.it")
    await db.commit()

    repository = AssociationRepository(db)
    found_subscription = await repository.get_subscription_by_user_email(
        "user_12345@pycon.it"
    )

    query = select(Subscription).where(Subscription.user_email == "user_12345@pycon.it")
    raw_query_subscription: Subscription = (
        await second_session.execute(query)
    ).scalar()

    # Check what we get executing the "raw query"
    # and what the repository returned. Is this the same thing?
    assert found_subscription.user_email == raw_query_subscription.user_email
    assert found_subscription.creation_date == raw_query_subscription.creation_date
    assert (
        found_subscription.stripe_session_id == raw_query_subscription.stripe_session_id
    )
    assert found_subscription.state == raw_query_subscription.state
    assert found_subscription.stripe_id == raw_query_subscription.stripe_id
    assert (
        found_subscription.stripe_customer_id
        == raw_query_subscription.stripe_customer_id
    )


@test("get subscription by session_id")
async def _(
    db=db,
    second_session=second_session,
    subscription_factory=subscription_factory,
    cleanup_db=cleanup_db,
):
    db = cast(AsyncSession, db)
    second_session = cast(AsyncSession, second_session)

    await subscription_factory(stripe_session_id="cs_test_12345")
    await db.commit()

    repository = AssociationRepository(db)
    found_subscription = await repository.get_subscription_by_session_id(
        "cs_test_12345"
    )

    query = select(Subscription).where(
        Subscription.stripe_session_id == "cs_test_12345"
    )
    raw_query_subscription: Subscription = (
        await second_session.execute(query)
    ).scalar()

    # Check what we get executing the "raw query"
    # and what the repository returned. Is this the same thing?
    assert found_subscription.user_id == raw_query_subscription.user_id
    assert found_subscription.creation_date == raw_query_subscription.creation_date
    assert (
        found_subscription.stripe_session_id == raw_query_subscription.stripe_session_id
    )
    assert found_subscription.state == raw_query_subscription.state
    assert found_subscription.stripe_id == raw_query_subscription.stripe_id
    assert (
        found_subscription.stripe_customer_id
        == raw_query_subscription.stripe_customer_id
    )


@test("get subscription by customer_id")
async def _(
    db=db,
    second_session=second_session,
    subscription_factory=subscription_factory,
    cleanup_db=cleanup_db,
):
    db = cast(AsyncSession, db)
    second_session = cast(AsyncSession, second_session)

    await subscription_factory(stripe_customer_id="cus_test_12345")
    await db.commit()

    repository = AssociationRepository(db)
    found_subscription = await repository.get_subscription_by_customer_id(
        "cus_test_12345"
    )

    query = select(Subscription).where(
        Subscription.stripe_customer_id == "cus_test_12345"
    )
    raw_query_subscription: Subscription = (
        await second_session.execute(query)
    ).scalar()

    # Check what we get executing the "raw query"
    # and what the repository returned. Is this the same thing?
    assert found_subscription.user_id == raw_query_subscription.user_id
    assert found_subscription.creation_date == raw_query_subscription.creation_date
    assert (
        found_subscription.stripe_session_id == raw_query_subscription.stripe_session_id
    )
    assert found_subscription.state == raw_query_subscription.state
    assert found_subscription.stripe_id == raw_query_subscription.stripe_id
    assert (
        found_subscription.stripe_customer_id
        == raw_query_subscription.stripe_customer_id
    )


@test("get subscription by stripe_id")
async def _(
    db=db,
    second_session=second_session,
    subscription_factory=subscription_factory,
    cleanup_db=cleanup_db,
):
    db = cast(AsyncSession, db)
    second_session = cast(AsyncSession, second_session)

    await subscription_factory(stripe_id="sub_test_12345")
    await db.commit()

    repository = AssociationRepository(db)
    found_subscription = await repository.get_subscription_by_stripe_id(
        "sub_test_12345"
    )

    query = select(Subscription).where(Subscription.stripe_id == "sub_test_12345")
    raw_query_subscription: Subscription = (
        await second_session.execute(query)
    ).scalar()

    # Check what we get executing the "raw query"
    # and what the repository returned. Is this the same thing?
    assert found_subscription.user_id == raw_query_subscription.user_id
    assert found_subscription.creation_date == raw_query_subscription.creation_date
    assert (
        found_subscription.stripe_session_id == raw_query_subscription.stripe_session_id
    )
    assert found_subscription.state == raw_query_subscription.state
    assert found_subscription.stripe_id == raw_query_subscription.stripe_id
    assert (
        found_subscription.stripe_customer_id
        == raw_query_subscription.stripe_customer_id
    )

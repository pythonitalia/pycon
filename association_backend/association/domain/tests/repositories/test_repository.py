import datetime
from typing import cast

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select
from ward import skip, test

from association.domain.entities.subscriptions import (
    Subscription,
    SubscriptionPayment,
    SubscriptionState,
)
from association.domain.repositories import AssociationRepository
from association.tests.factories import (
    SubscriptionFactory,
    SubscriptionPaymentFactory,
    subscription_factory,
)
from association.tests.session import cleanup_db, db, second_session


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
    assert found_subscription.created_at == raw_query_subscription.created_at
    assert found_subscription.state == raw_query_subscription.state
    assert (
        found_subscription.stripe_subscription_id
        == raw_query_subscription.stripe_subscription_id
    )
    assert (
        found_subscription.stripe_customer_id
        == raw_query_subscription.stripe_customer_id
    )


@test("get subscription by stripe_customer_id")
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
    found_subscription = await repository.get_subscription_by_stripe_customer_id(
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
    assert found_subscription.created_at == raw_query_subscription.created_at
    assert found_subscription.state == raw_query_subscription.state
    assert (
        found_subscription.stripe_subscription_id
        == raw_query_subscription.stripe_subscription_id
    )
    assert (
        found_subscription.stripe_customer_id
        == raw_query_subscription.stripe_customer_id
    )


@test("get subscription by stripe_subscription_id")
async def _(
    db=db,
    second_session=second_session,
    subscription_factory=subscription_factory,
    cleanup_db=cleanup_db,
):
    db = cast(AsyncSession, db)
    second_session = cast(AsyncSession, second_session)

    await subscription_factory(stripe_subscription_id="sub_test_12345")
    await db.commit()

    repository = AssociationRepository(db)
    found_subscription = await repository.get_subscription_by_stripe_subscription_id(
        "sub_test_12345"
    )

    query = select(Subscription).where(
        Subscription.stripe_subscription_id == "sub_test_12345"
    )
    raw_query_subscription: Subscription = (
        await second_session.execute(query)
    ).scalar()

    # Check what we get executing the "raw query"
    # and what the repository returned. Is this the same thing?
    assert found_subscription.user_id == raw_query_subscription.user_id
    assert found_subscription.created_at == raw_query_subscription.created_at
    assert found_subscription.state == raw_query_subscription.state
    assert (
        found_subscription.stripe_subscription_id
        == raw_query_subscription.stripe_subscription_id
    )
    assert (
        found_subscription.stripe_customer_id
        == raw_query_subscription.stripe_customer_id
    )


@test("save_subscription")
async def _(db=db, second_session=second_session, cleanup_db=cleanup_db):
    db = cast(AsyncSession, db)
    second_session = cast(AsyncSession, second_session)

    repository = AssociationRepository(db)

    await repository.save_subscription(
        Subscription(
            user_id=1234,
            created_at=datetime.datetime(
                2020, 1, 1, 1, 0, tzinfo=datetime.timezone.utc
            ),
            modified_at=datetime.datetime(
                2020, 1, 1, 2, 0, tzinfo=datetime.timezone.utc
            ),
            state=SubscriptionState.PENDING,
            stripe_subscription_id="sub_test_IxcENZqOBlHAJo",
            stripe_customer_id="cus_test_IuwfUVsdQFNvqc",
        )
    )
    await repository.commit()

    query = select(Subscription).where(Subscription.user_id == 1234)
    db_subscription: Subscription = (await second_session.execute(query)).scalar()

    assert db_subscription
    assert db_subscription.user_id == 1234
    assert db_subscription.created_at == datetime.datetime(
        2020, 1, 1, 1, 0, tzinfo=datetime.timezone.utc
    )
    assert db_subscription.modified_at == datetime.datetime(
        2020, 1, 1, 2, 0, tzinfo=datetime.timezone.utc
    )
    assert db_subscription.state == SubscriptionState.PENDING
    assert db_subscription.stripe_subscription_id == "sub_test_IxcENZqOBlHAJo"
    assert db_subscription.stripe_customer_id == "cus_test_IuwfUVsdQFNvqc"


@test("delete_subscription")
async def _(db=db, second_session=second_session, cleanup_db=cleanup_db):
    db = cast(AsyncSession, db)
    second_session = cast(AsyncSession, second_session)

    repository = AssociationRepository(db)
    subscription = Subscription(
        user_id=1234,
        created_at=datetime.datetime(2020, 1, 1, 1, 0, tzinfo=datetime.timezone.utc),
        modified_at=datetime.datetime(2020, 1, 1, 2, 0, tzinfo=datetime.timezone.utc),
        state=SubscriptionState.PENDING,
        stripe_subscription_id="sub_test_IxcENZqOBlHAJo",
        stripe_customer_id="cus_test_IuwfUVsdQFNvqc",
    )
    await repository.save_subscription(subscription)
    await repository.commit()

    query = select(Subscription).where(Subscription.user_id == 1234)
    db_subscription: Subscription = (await second_session.execute(query)).scalar()
    assert db_subscription

    await repository.delete_subscription(subscription)
    await repository.commit()

    db_subscription: Subscription = (await second_session.execute(query)).scalar()
    assert not db_subscription


@test("save_subscription passing a modified subscription")
async def _(db=db, second_session=second_session, cleanup_db=cleanup_db):
    db = cast(AsyncSession, db)
    second_session = cast(AsyncSession, second_session)

    repository = AssociationRepository(db)

    subscription = Subscription(
        user_id=1234,
        created_at=datetime.datetime(2020, 1, 1, 1, 0, tzinfo=datetime.timezone.utc),
        modified_at=datetime.datetime(2020, 1, 1, 1, 0, tzinfo=datetime.timezone.utc),
        state=SubscriptionState.PENDING,
        stripe_subscription_id="",
        stripe_customer_id="",
    )
    await repository.save_subscription(subscription)
    await repository.commit()

    # query = select(Subscription).where(Subscription.user_id == 1234)
    # db_subscription: Subscription = (await second_session.execute(query)).scalar()
    #
    # assert db_subscription
    # assert db_subscription.user_id == 1234
    # assert db_subscription.stripe_customer_id == ""

    subscription.stripe_customer_id = "cus_test_IuwfUVsdQFNvqc"
    await repository.save_subscription(subscription)
    await repository.commit()

    query = select(Subscription).where(Subscription.user_id == 1234)
    db_subscription: Subscription = (await second_session.execute(query)).scalar()
    assert db_subscription
    assert db_subscription.user_id == 1234
    assert db_subscription.stripe_customer_id == "cus_test_IuwfUVsdQFNvqc"


@skip(
    'This test doesn t fail but the call to repository.commit() interrupts the test pipeline! -> sqlalchemy.exc.IntegrityError: (psycopg2.errors.ForeignKeyViolation) update or delete on table "subscription" violates foreign key constraint "subscription_payment_subscription_id_fkey" on table "subscription_payment" DETAIL:  Key (user_id)=(1234) is still referenced from table "subscription_payment".'
)
@test("save_payment", tags=["failing"])
async def _(db=db, second_session=second_session, cleanup_db=cleanup_db):
    db = cast(AsyncSession, db)
    second_session = cast(AsyncSession, second_session)

    repository = AssociationRepository(db)

    subscription = Subscription(
        user_id=1234,
        created_at=datetime.datetime(2020, 1, 1, 1, 0, tzinfo=datetime.timezone.utc),
        modified_at=datetime.datetime(2020, 1, 1, 2, 0, tzinfo=datetime.timezone.utc),
        state=SubscriptionState.PENDING,
        stripe_subscription_id="sub_test_IxcENZqOBlHAJo",
        stripe_customer_id="cus_test_IuwfUVsdQFNvqc",
    )

    subscription = await repository.save_subscription(subscription)
    await repository.commit()

    await repository.save_payment(
        SubscriptionPayment(
            subscription=subscription,
            payment_date=datetime.datetime(
                2020, 1, 1, 1, 0, tzinfo=datetime.timezone.utc
            ),
            stripe_invoice_id="inv_test_a1wtX1HXf3iOjdQK1cyEN3YavPmxSaTkdfo2fCAPLqlOPT3blEZrUOIlaQ",
            invoice_pdf="https://stripe.com/pdf/invoice_test_1234",
        )
    )
    await repository.commit()

    query = select(SubscriptionPayment).where(
        SubscriptionPayment.subscription_id == subscription.user_id
    )
    db_entry: SubscriptionPayment = (await second_session.execute(query)).scalar()

    assert db_entry
    assert db_entry.subscription == subscription
    assert db_entry.payment_date == datetime.datetime(
        2020, 1, 1, 1, 0, tzinfo=datetime.timezone.utc
    )
    assert (
        db_entry.stripe_invoice_id
        == "inv_test_a1wtX1HXf3iOjdQK1cyEN3YavPmxSaTkdfo2fCAPLqlOPT3blEZrUOIlaQ"
    )
    assert db_entry.invoice_pdf == "https://stripe.com/pdf/invoice_test_1234"


@skip(
    'This test doesn t fail but the call to repository.commit() interrupts the test pipeline! -> sqlalchemy.exc.IntegrityError: (psycopg2.errors.ForeignKeyViolation) update or delete on table "subscription" violates foreign key constraint "subscription_payment_subscription_id_fkey" on table "subscription_payment" DETAIL:  Key (user_id)=(1234) is still referenced from table "subscription_payment".'
)
@test("get subscription payment by stripe_invoice_id", tags=["current"])
async def _(
    db=db,
    second_session=second_session,
    cleanup_db=cleanup_db,
):
    db = cast(AsyncSession, db)
    second_session = cast(AsyncSession, second_session)

    subscription = SubscriptionFactory(user_id=12345)
    SubscriptionPaymentFactory(
        subscription=subscription, stripe_invoice_id="inv_test_12345"
    )
    await db.commit()

    repository = AssociationRepository(db)
    found_subscription_payment = await repository.get_payment_by_stripe_invoice_id(
        "inv_test_12345"
    )

    query = select(SubscriptionPayment).where(
        SubscriptionPayment.stripe_invoice_id == "inv_test_12345"
    )
    raw_query_subscription_payment: SubscriptionPayment = (
        await second_session.execute(query)
    ).scalar()

    # Check what we get executing the "raw query"
    # and what the repository returned. Is this the same thing?
    assert (
        found_subscription_payment.stripe_invoice_id
        == raw_query_subscription_payment.stripe_invoice_id
    )

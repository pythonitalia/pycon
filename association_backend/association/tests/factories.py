import asyncio
import inspect
import string

import factory.fuzzy
from factory.alchemy import SQLAlchemyModelFactory
from faker.providers import BaseProvider
from ward import fixture

from association.domain.entities import (
    Subscription,
    SubscriptionPayment,
    SubscriptionState,
)
from association.domain.entities.stripe import (
    StripeCheckoutSession,
    StripeCustomer,
    StripeSubscription,
    StripeSubscriptionStatus,
)

from .session import test_session


class StripeProvider(BaseProvider):
    """

    @factory.lazy_attribute
    def customer_code(self):
        from faker import Factory
        from association.factories import StripeProvider as Provider
        fake = Factory.create()
        fake.add_provider(Provider)
        return fake.customer_code()

    """

    def customer_id(self):
        return "cus_test_" + "".join(
            self.random_elements(string.ascii_lowercase + string.digits, length=16)
        )

    def checkout_session_id(self):
        return "cs_test_" + "".join(
            self.random_elements(string.ascii_lowercase + string.digits, length=16)
        )

    def subscription_id(self):
        return "sub_test_" + "".join(
            self.random_elements(string.ascii_lowercase + string.digits, length=16)
        )

    def stripe_invoice_id(self):
        return "inv_test_" + "".join(
            self.random_elements(string.ascii_lowercase + string.digits, length=16)
        )

    def invoice_pdf(self):
        return "https://python-italia.stripe.com/invoices/{invoice_code}.pdf" "".format(
            invoice_code=self.stripe_invoice_id()
        )

    def customer_portal_session_id(self):
        return "https://stripe.com/stripe_test_customer_portal/" + "".join(
            self.random_elements(string.ascii_lowercase + string.digits, length=16)
        )


class AsyncFactory(SQLAlchemyModelFactory):
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        async def maker_coroutine():
            for key, value in kwargs.items():
                # when using SubFactory, you'll have a Task in the corresponding kwarg
                # await tasks to pass model instances instead
                if inspect.isawaitable(value):
                    kwargs[key] = await value
            # replace as needed by your way of creating model instances
            return await model_class.create_async(*args, **kwargs)

        # A Task can be awaited multiple times, unlike a coroutine.
        # useful when a factory and a subfactory must share a same object
        return asyncio.create_task(maker_coroutine())

    @classmethod
    async def create_batch(cls, size, **kwargs):
        return [await cls.create(**kwargs) for _ in range(size)]


class SubscriptionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Subscription
        sqlalchemy_session = test_session

    user_id = factory.Faker("pyint", min_value=1)
    created_at = factory.Faker("date_between", start_date="-30y", end_date="today")
    modified_at = factory.Faker("date_between", start_date="-30y", end_date="today")
    state = factory.fuzzy.FuzzyChoice(SubscriptionState)

    class Params:
        with_manageable_subscription = factory.Trait(
            state=factory.fuzzy.FuzzyChoice(
                [SubscriptionState.ACTIVE, SubscriptionState.EXPIRED]
            ),
        )
        without_manageable_subscription = factory.Trait(
            state=SubscriptionState.CANCELED,
        )
        without_subscription = factory.Trait(
            state=SubscriptionState.PENDING, stripe_subscription_id=""
        )
        canceled = factory.Trait(
            state=SubscriptionState.CANCELED,
            # canceled_at=factory.Faker("date_between", start_date="-1y", end_date="today")
        )

    @factory.lazy_attribute
    def stripe_subscription_id(self):
        from faker import Factory

        fake = Factory.create()
        fake.add_provider(StripeProvider)
        return fake.subscription_id()

    @factory.lazy_attribute
    def stripe_customer_id(self):
        from faker import Factory

        fake = Factory.create()
        fake.add_provider(StripeProvider)
        return fake.customer_id()


@fixture
async def subscription_factory():
    async def func(**kwargs):
        obj = SubscriptionFactory.create(**kwargs)
        await SubscriptionFactory._meta.sqlalchemy_session.flush()
        return obj

    return func


@fixture
async def subscription_factory_batch():
    async def func(**kwargs):
        obj = SubscriptionFactory.create_batch(**kwargs)
        await SubscriptionFactory._meta.sqlalchemy_session.flush()
        return obj

    return func


class SubscriptionPaymentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = SubscriptionPayment
        sqlalchemy_session = test_session

    payment_date = factory.Faker("date_between", start_date="-7d", end_date="today")
    subscription = factory.SubFactory(SubscriptionFactory)

    # @factory.lazy_attribute
    # def subscription(self):
    #     from faker import Factory
    #
    #     fake = Factory.create()
    #     fake.add_provider(StripeProvider)
    #     return fake.subscription_id()

    @factory.lazy_attribute
    def stripe_invoice_id(self):
        from faker import Factory

        fake = Factory.create()
        fake.add_provider(StripeProvider)
        return fake.stripe_invoice_id()

    @factory.lazy_attribute
    def invoice_pdf(self):
        from faker import Factory

        fake = Factory.create()
        fake.add_provider(StripeProvider)
        return fake.invoice_pdf()


class CustomerFactory(SQLAlchemyModelFactory):
    class Meta:
        model = StripeCustomer
        sqlalchemy_session = test_session

    @factory.lazy_attribute
    def id(self):
        from faker import Factory

        fake = Factory.create()
        fake.add_provider(StripeProvider)
        return fake.customer_id()


class StripeCheckoutSessionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = StripeCheckoutSession
        sqlalchemy_session = test_session

    @factory.lazy_attribute
    def id(self):
        from faker import Factory

        fake = Factory.create()
        fake.add_provider(StripeProvider)
        return fake.checkout_session_id()

    @factory.lazy_attribute
    def subscription_id(self):
        from faker import Factory

        fake = Factory.create()
        fake.add_provider(StripeProvider)
        return fake.subscription_id()

    @factory.lazy_attribute
    def customer_id(self):
        from faker import Factory

        fake = Factory.create()
        fake.add_provider(StripeProvider)
        return fake.customer_id()


class StripeSubscriptionFactory(SQLAlchemyModelFactory):
    status = factory.fuzzy.FuzzyChoice(StripeSubscriptionStatus)

    class Meta:
        model = StripeSubscription
        sqlalchemy_session = test_session

    @factory.lazy_attribute
    def id(self):
        from faker import Factory

        fake = Factory.create()
        fake.add_provider(StripeProvider)
        return fake.subscription_id()

    @factory.lazy_attribute
    def customer_id(self):
        from faker import Factory

        fake = Factory.create()
        fake.add_provider(StripeProvider)
        return fake.customer_id()


class StripeCustomerFactory(SQLAlchemyModelFactory):
    email = factory.Faker("ascii_safe_email")

    class Meta:
        model = StripeCustomer
        sqlalchemy_session = test_session

    @factory.lazy_attribute
    def id(self):
        from faker import Factory

        fake = Factory.create()
        fake.add_provider(StripeProvider)
        return fake.customer_id()

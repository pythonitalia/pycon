import asyncio
import inspect
import string

import factory.fuzzy
from association.domain.entities import Subscription, SubscriptionState
from factory.alchemy import SQLAlchemyModelFactory
from faker.providers import BaseProvider
from ward import fixture

from ..domain.entities.stripe_entities import StripeCheckoutSession, StripeCustomer
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
        return (
            "cus_test_"
            + self.random_elements(string.ascii_lowercase + string.digits, length=16)[0]
        )

    def checkout_session_id(self):
        return (
            "cs_test_"
            + self.random_elements(string.ascii_lowercase + string.digits, length=16)[0]
        )

    def subscription_id(self):
        return (
            "sub_test_"
            + self.random_elements(string.ascii_lowercase + string.digits, length=16)[0]
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

    user_id = factory.Faker("pystr", min_chars=5, max_chars=8)
    creation_date = factory.Faker("date_between", start_date="-30y", end_date="today")
    payment_date = factory.Faker("date_between", start_date="-30y", end_date="today")
    expiration_date = factory.Faker("date_between", start_date="-5y", end_date="today")
    state = factory.fuzzy.FuzzyChoice(SubscriptionState)

    # stripe_id = factory.Faker("pystr", min_chars=5, max_chars=8)
    # stripe_customer_id = factory.Faker("pystr", min_chars=5, max_chars=8)
    # stripe_session_id = factory.Faker("pystr", min_chars=5, max_chars=8)

    @factory.lazy_attribute
    def stripe_id(self):
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

    @factory.lazy_attribute
    def stripe_session_id(self):
        from faker import Factory

        fake = Factory.create()
        fake.add_provider(StripeProvider)
        return fake.checkout_session_id()


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

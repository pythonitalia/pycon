import string

import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker.providers import BaseProvider
from ward import fixture

from ..domain.entities import Subscription
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
        return "cus_test_" + self.random_elements(
            string.ascii_lowercase + string.digits, length=16
        )

    def checkout_session_id(self):
        return "cs_test_" + self.random_elements(
            string.ascii_lowercase + string.digits, length=16
        )

    def subscription_id(self):
        return "sub_test_" + self.random_elements(
            string.ascii_lowercase + string.digits, length=16
        )


class SubscriptionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Subscription
        sqlalchemy_session = test_session

    creation_date = factory.Faker("date_between", start_date="-30y", end_date="today")
    payment_date = factory.Faker("date_between", start_date="-30y", end_date="today")

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

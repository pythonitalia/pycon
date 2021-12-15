from datetime import timezone

import factory
from faker import Faker

from src.association.tests.factories import ModelFactory
from src.association_membership.domain.entities import StripeCustomer, Subscription

fake = Faker()


class SubscriptionFactory(ModelFactory):
    class Meta:
        model = Subscription


class StripeCustomerFactory(ModelFactory):
    class Meta:
        model = StripeCustomer

    stripe_customer_id = factory.LazyAttribute(lambda _: f"cus_{fake.uuid4()}")

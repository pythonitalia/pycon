from datetime import timezone

import factory
from faker import Faker

from src.association.tests.factories import ModelFactory
from src.association_membership.domain.entities import Subscription

fake = Faker()


class SubscriptionFactory(ModelFactory):
    class Meta:
        model = Subscription

#    stripe_subscription_id = factory.LazyAttribute(lambda _: f"sub_{fake.uuid4()}")

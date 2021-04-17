import factory
from faker import Faker

from association.tests.factories import ModelFactory
from association_membership.domain.entities import Subscription
from customers.tests.factories import CustomerFactory

fake = Faker()


class SubscriptionFactory(ModelFactory):
    class Meta:
        model = Subscription

    customer = factory.SubFactory(CustomerFactory)
    stripe_subscription_id = factory.LazyAttribute(lambda _: f"sub_{fake.uuid4()}")

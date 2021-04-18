import factory
from faker import Faker

from src.association.tests.factories import ModelFactory
from src.customers.domain.entities import Customer

fake = Faker()


class CustomerFactory(ModelFactory):
    class Meta:
        model = Customer

    user_id = factory.LazyAttribute(lambda _: fake.pyint(min_value=1, max_value=1000))
    stripe_customer_id = factory.LazyAttribute(lambda obj: f"cus_{obj.user_id}")

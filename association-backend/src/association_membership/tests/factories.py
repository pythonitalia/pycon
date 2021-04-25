from datetime import timezone

import factory
from faker import Faker

from src.association.tests.factories import ModelFactory
from src.association_membership.domain.entities import Subscription, SubscriptionInvoice
from src.customers.tests.factories import CustomerFactory

fake = Faker()


class SubscriptionFactory(ModelFactory):
    class Meta:
        model = Subscription

    customer = factory.SubFactory(CustomerFactory)
    stripe_subscription_id = factory.LazyAttribute(lambda _: f"sub_{fake.uuid4()}")


class SubscriptionInvoiceFactory(ModelFactory):
    class Meta:
        model = SubscriptionInvoice

    subscription = factory.SubFactory(SubscriptionFactory)
    payment_date = factory.LazyAttribute(
        lambda _: fake.past_datetime(start_date="-5d", tzinfo=timezone.utc)
    )
    period_start = factory.LazyAttribute(
        lambda _: fake.past_datetime(start_date="-4d", tzinfo=timezone.utc)
    )
    period_end = factory.LazyAttribute(
        lambda _: fake.future_datetime(end_date="+30d", tzinfo=timezone.utc)
    )
    stripe_invoice_id = factory.LazyAttribute(lambda _: f"in_{fake.uuid4()}")
    invoice_pdf = "https://example.org/fake-stripe-invoice"

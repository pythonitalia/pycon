from factory.django import DjangoModelFactory
import factory


from association_membership.models import StripeCustomer, Subscription
from users.tests.factories import UserFactory


class SubscriptionFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Subscription


class StripeCustomerFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = StripeCustomer

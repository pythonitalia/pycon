from factory.django import DjangoModelFactory
import factory


from association_membership.models import StripeCustomer, Membership
from users.tests.factories import UserFactory


class MembershipFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Membership


class StripeCustomerFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = StripeCustomer

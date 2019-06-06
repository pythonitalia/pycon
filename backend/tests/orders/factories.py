import pytz
import factory
import factory.fuzzy

from pytest_factoryboy import register

from factory.django import DjangoModelFactory

from tests.users.factories import UserFactory

from orders.models import Order


@register
class OrderFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    amount = factory.Faker('pydecimal', positive=True, left_digits=None, right_digits=None)

    class Meta:
        model = Order

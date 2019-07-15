import pytz
import factory
import factory.fuzzy

from decimal import Decimal

from pytest_factoryboy import register

from factory.django import DjangoModelFactory

from tests.users.factories import UserFactory

from orders.models import Order, OrderItem


@register
class OrderFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    amount = Decimal('100')

    class Meta:
        model = Order


@register
class OrderItemFactory(DjangoModelFactory):
    order = factory.SubFactory(OrderFactory)
    quantity = factory.Faker('pyint')

    class Meta:
        model = OrderItem

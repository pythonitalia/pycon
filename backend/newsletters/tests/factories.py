import factory
from factory.django import DjangoModelFactory
from newsletters.models import Subscription
from pytest_factoryboy import register


@register
class SubscriptionFactory(DjangoModelFactory):
    class Meta:
        model = Subscription
        django_get_or_create = ("email",)

    email = factory.Faker("email")

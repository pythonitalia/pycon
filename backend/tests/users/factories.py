import factory

from pytest_factoryboy import register
from factory.django import DjangoModelFactory

from users.models import User


@register
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('email')
    username = factory.Faker('user_name')

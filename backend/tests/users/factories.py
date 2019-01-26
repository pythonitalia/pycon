import factory
import factory.fuzzy

from pytest_factoryboy import register

from factory.django import DjangoModelFactory

from users.models import User


@register
class UserFactory(DjangoModelFactory):
    email = factory.Faker('email')
    username = factory.Faker('user_name')

    is_active = True
    is_staff = False

    class Meta:
        model = User
        django_get_or_create = ('email',)

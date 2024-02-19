import factory
import factory.fuzzy
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from users.models import User


@register
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("word")
    email = factory.Faker("email")
    full_name = factory.Faker("name")
    password = factory.PostGenerationMethodCall("set_password", "test")

    @classmethod
    def _after_postgeneration(cls, obj, create, results=None):
        if create and results:
            obj.save()

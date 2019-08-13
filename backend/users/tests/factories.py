import factory
import factory.fuzzy
from factory.django import DjangoModelFactory
from pytest_factoryboy import register
from users.models import User


@register
class UserFactory(DjangoModelFactory):
    email = factory.Faker("email")
    name = factory.Faker("first_name")
    full_name = factory.Faker("name")
    username = factory.Faker("user_name")

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    password = factory.PostGenerationMethodCall("set_password", "defaultpassword")

    is_active = True
    is_staff = False

    class Meta:
        model = User
        django_get_or_create = ("email",)

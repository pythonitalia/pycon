import datetime

import factory
import factory.fuzzy
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from users.models import COUNTRIES, User


@register
class UserFactory(DjangoModelFactory):

    email = factory.Faker("email")
    name = factory.Faker("first_name")
    full_name = factory.Faker("name")
    username = factory.Faker("user_name")

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    gender = factory.fuzzy.FuzzyChoice(["male", "female"])
    open_to_recruiting = False

    date_birth = factory.fuzzy.FuzzyDate(
        start_date=datetime.date(1, 1, 1),
        end_date=datetime.date.today() - datetime.timedelta(days=20 * 365),
    )

    password = factory.PostGenerationMethodCall("set_password", "defaultpassword")
    country = factory.fuzzy.FuzzyChoice(COUNTRIES, getter=lambda c: c["code"])

    is_active = True
    is_staff = False

    class Meta:
        model = User
        django_get_or_create = ("email",)

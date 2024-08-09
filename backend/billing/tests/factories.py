from organizers.tests.factories import OrganizerFactory
from users.tests.factories import UserFactory
import factory
import factory.fuzzy

from billing.models import BillingAddress
from factory.django import DjangoModelFactory


class BillingAddressFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    organizer = factory.SubFactory(OrganizerFactory)
    is_business = False
    company_name = factory.Faker("text")
    user_name = factory.Faker("text")
    zip_code = factory.Faker("text")
    city = factory.Faker("text")
    address = factory.Faker("text")
    country = "IT"
    vat_id = ""
    fiscal_code = ""
    sdi = ""
    pec = ""

    class Meta:
        model = BillingAddress

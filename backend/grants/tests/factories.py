import factory.fuzzy
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from conferences.tests.factories import ConferenceFactory
from grants.models import GRANT_TYPES, INTERESTED_IN_VOLUNTEERING, OCCUPATIONS, Grant
from helpers.constants import GENDERS


@register
class GrantFactory(DjangoModelFactory):
    class Meta:
        model = Grant

    name = factory.Faker("first_name")
    full_name = factory.Faker("name")
    conference = factory.SubFactory(ConferenceFactory)
    email = factory.Faker("email")
    user_id = factory.Faker("pyint")
    age_group = factory.fuzzy.FuzzyChoice(Grant.AgeGroup)
    gender = factory.fuzzy.FuzzyChoice([gender[0] for gender in GENDERS])
    occupation = factory.fuzzy.FuzzyChoice(
        [occupation[0] for occupation in OCCUPATIONS]
    )
    grant_type = factory.fuzzy.FuzzyChoice(
        [grant_type[0] for grant_type in GRANT_TYPES]
    )

    python_usage = factory.Faker("text")
    been_to_other_events = factory.Faker("text")
    interested_in_volunteering = factory.fuzzy.FuzzyChoice(
        [interested[0] for interested in INTERESTED_IN_VOLUNTEERING]
    )
    needs_funds_for_travel = factory.Faker("boolean")
    why = factory.Faker("text")
    notes = factory.Faker("text")
    travelling_from = factory.Faker("country")

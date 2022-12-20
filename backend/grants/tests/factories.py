import factory.fuzzy
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from conferences.tests.factories import ConferenceFactory
from grants.models import Grant
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
    occupation = factory.fuzzy.FuzzyChoice(Grant.Occupation)
    grant_type = factory.fuzzy.FuzzyChoice(Grant.GrantType)

    python_usage = factory.Faker("text")
    been_to_other_events = factory.Faker("text")
    interested_in_volunteering = factory.fuzzy.FuzzyChoice(
        Grant.InterestedInVolunteering
    )
    needs_funds_for_travel = factory.Faker("boolean")
    why = factory.Faker("text")
    notes = factory.Faker("text")
    travelling_from = factory.Faker("country")

import factory.fuzzy
from factory.django import DjangoModelFactory

from conferences.tests.factories import ConferenceFactory
from grants.models import Grant
from helpers.constants import GENDERS
from users.tests.factories import UserFactory
from countries import countries
from participants.tests.factories import ParticipantFactory
from participants.models import Participant


class GrantFactory(DjangoModelFactory):
    class Meta:
        model = Grant

    name = factory.Faker("first_name")
    full_name = factory.Faker("name")
    conference = factory.SubFactory(ConferenceFactory)
    email = factory.Faker("email")
    user = factory.SubFactory(UserFactory)
    age_group = factory.fuzzy.FuzzyChoice(Grant.AgeGroup)
    gender = factory.fuzzy.FuzzyChoice([gender[0] for gender in GENDERS])
    occupation = factory.fuzzy.FuzzyChoice(Grant.Occupation)
    grant_type = factory.fuzzy.FuzzyChoice(Grant.GrantType)

    python_usage = factory.Faker("text")
    been_to_other_events = factory.Faker("text")

    needs_funds_for_travel = factory.Faker("boolean")
    why = factory.Faker("text")
    notes = factory.Faker("text")
    travelling_from = factory.fuzzy.FuzzyChoice([country.code for country in countries])
    website = factory.Faker("url")
    twitter_handle = "@handle"
    github_handle = factory.Faker("user_name")
    linkedin_url = factory.Faker("user_name")
    mastodon_handle = factory.Faker("user_name")

    @classmethod
    def _create(self, model_class, *args, **kwargs):
        grant = super()._create(model_class, *args, **kwargs)

        if not Participant.objects.filter(
            user_id=grant.user.id, conference=grant.conference
        ).exists():
            ParticipantFactory(user_id=grant.user.id, conference=grant.conference)

        return grant

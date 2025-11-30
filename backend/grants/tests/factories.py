import random
from decimal import Decimal

import factory.fuzzy
from factory.django import DjangoModelFactory

from conferences.tests.factories import ConferenceFactory
from countries import countries
from grants.models import Grant, GrantReimbursement, GrantReimbursementCategory
from helpers.constants import GENDERS
from participants.models import Participant
from participants.tests.factories import ParticipantFactory
from users.tests.factories import UserFactory


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
    grant_type = factory.LazyFunction(
        lambda: random.sample(
            [choice[0] for choice in Grant.GrantType.choices],
            k=random.randint(1, len(Grant.GrantType.choices)),
        )
    )

    python_usage = factory.Faker("text")
    been_to_other_events = factory.Faker("text")

    needs_funds_for_travel = factory.Faker("boolean")
    why = factory.Faker("text")
    notes = factory.Faker("text")
    departure_country = factory.fuzzy.FuzzyChoice(
        [country.code for country in countries]
    )
    nationality = factory.Faker("country")
    departure_city = factory.Faker("city")
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


class GrantReimbursementCategoryFactory(DjangoModelFactory):
    class Meta:
        model = GrantReimbursementCategory

    conference = factory.SubFactory(ConferenceFactory)
    name = factory.LazyAttribute(
        lambda obj: GrantReimbursementCategory.Category(obj.category).label
    )
    description = factory.Faker("sentence", nb_words=6)
    max_amount = factory.fuzzy.FuzzyInteger(0, 1000)
    category = factory.fuzzy.FuzzyChoice(
        [choice[0] for choice in GrantReimbursementCategory.Category.choices]
    )
    included_by_default = False

    class Params:
        ticket = factory.Trait(
            category=GrantReimbursementCategory.Category.TICKET,
            name="Ticket",
            max_amount=Decimal("100"),
            included_by_default=True,
        )
        travel = factory.Trait(
            category=GrantReimbursementCategory.Category.TRAVEL,
            name="Travel",
            max_amount=Decimal("500"),
            included_by_default=False,
        )
        accommodation = factory.Trait(
            category=GrantReimbursementCategory.Category.ACCOMMODATION,
            name="Accommodation",
            max_amount=Decimal("300"),
            included_by_default=False,
        )
        other = factory.Trait(
            category=GrantReimbursementCategory.Category.OTHER,
            name="Other",
            max_amount=Decimal("200"),
            included_by_default=False,
        )


class GrantReimbursementFactory(DjangoModelFactory):
    class Meta:
        model = GrantReimbursement

    grant = factory.SubFactory(GrantFactory)
    category = factory.SubFactory(GrantReimbursementCategoryFactory)
    granted_amount = factory.fuzzy.FuzzyInteger(0, 1000)

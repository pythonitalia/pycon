import factory
import factory.fuzzy
from factory.django import DjangoModelFactory

from conferences.tests.factories import ConferenceFactory
from pycon.constants import COLORS
from sponsors.models import (
    Sponsor,
    SponsorBenefit,
    SponsorLead,
    SponsorLevel,
    SponsorLevelBenefit,
    SponsorSpecialOption,
)


class SponsorFactory(DjangoModelFactory):
    name = factory.Faker("word")
    link = factory.Faker("url")
    image = factory.django.ImageField()
    order = factory.Faker("pyint", min_value=0)

    @classmethod
    def _after_postgeneration(cls, obj, create, results=None):
        if create and results:
            obj.save()

    class Meta:
        model = Sponsor


class SponsorLevelFactory(DjangoModelFactory):
    name = factory.Faker("word")
    conference = factory.SubFactory(ConferenceFactory)
    highlight_color = factory.fuzzy.FuzzyChoice([color[0] for color in COLORS])

    @classmethod
    def _after_postgeneration(cls, obj, create, results=None):
        if create and results:
            obj.save()

    class Meta:
        model = SponsorLevel

    @factory.post_generation
    def sponsors(self, create, extracted, **kwargs):
        """Accepts a list of sponsors and adds each sponsor to the SponsorLevel"""
        if not create:
            return

        if extracted:
            for sponsor in extracted:
                self.sponsors.add(sponsor)


class SponsorLeadFactory(DjangoModelFactory):
    fullname = factory.Faker("name")
    email = factory.Faker("email")
    company = factory.Faker("company")
    conference = factory.SubFactory(ConferenceFactory)
    consent_to_contact_via_email = factory.Faker("boolean")
    brochure_viewed = factory.Faker("boolean")

    class Meta:
        model = SponsorLead


class SponsorBenefitFactory(DjangoModelFactory):
    name = factory.Faker("word")
    category = factory.Faker("word")
    description = factory.Faker("text")
    conference = factory.SubFactory(ConferenceFactory)

    class Meta:
        model = SponsorBenefit


class SponsorLevelBenefitFactory(DjangoModelFactory):
    value = factory.Faker("word")
    benefit = factory.SubFactory(SponsorBenefitFactory)
    sponsor_level = factory.SubFactory(SponsorLevelFactory)

    class Meta:
        model = SponsorLevelBenefit


class SponsorSpecialOptionFactory(DjangoModelFactory):
    name = factory.Faker("word")
    description = factory.Faker("text")
    price = factory.Faker("pyint")

    class Meta:
        model = SponsorSpecialOption

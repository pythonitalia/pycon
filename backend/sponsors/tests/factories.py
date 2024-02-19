import factory
import factory.fuzzy
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from conferences.tests.factories import ConferenceFactory
from pycon.constants import COLORS
from sponsors.models import Sponsor, SponsorLead, SponsorLevel


@register
class SponsorFactory(DjangoModelFactory):
    name = factory.Faker("word")
    link = factory.Faker("url")
    image = factory.django.ImageField()
    order = factory.Faker("pyint", min_value=0)

    class Meta:
        model = Sponsor
        skip_postgeneration_save = True


@register
class SponsorLevelFactory(DjangoModelFactory):
    name = factory.Faker("word")
    conference = factory.SubFactory(ConferenceFactory)
    highlight_color = factory.fuzzy.FuzzyChoice([color[0] for color in COLORS])

    class Meta:
        model = SponsorLevel
        skip_postgeneration_save = True

    @factory.post_generation
    def sponsors(self, create, extracted, **kwargs):
        """Accepts a list of sponsors and adds each sponsor to the SponsorLevel"""
        if not create:
            return

        if extracted:
            for sponsor in extracted:
                self.sponsors.add(sponsor)


@register
class SponsorLeadFactory(DjangoModelFactory):
    fullname = factory.Faker("name")
    email = factory.Faker("email")
    company = factory.Faker("company")
    conference = factory.SubFactory(ConferenceFactory)
    consent_to_contact_via_email = factory.Faker("boolean")
    brochure_viewed = factory.Faker("boolean")

    class Meta:
        model = SponsorLead

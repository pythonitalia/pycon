import factory
import factory.fuzzy
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from conferences.tests.factories import ConferenceFactory
from i18n.tests.factories import LanguageFactory
from job_board.models import JobListing


@register
class JobListingFactory(DjangoModelFactory):
    title = LanguageFactory("sentence")
    slug = LanguageFactory("slug")
    description = LanguageFactory("sentence")
    company = LanguageFactory("sentence")
    company_logo = factory.django.ImageField()
    conference = factory.SubFactory(ConferenceFactory)

    class Meta:
        model = JobListing

import factory
import factory.fuzzy
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from job_board.models import JobListing
from i18n.tests.factories import LanguageFactory


@register
class JobListingFactory(DjangoModelFactory):
    title = LanguageFactory("sentence")
    slug = LanguageFactory("slug")
    description = LanguageFactory("sentence")
    company = LanguageFactory("sentence")
    company_logo = factory.django.ImageField()

    class Meta:
        model = JobListing

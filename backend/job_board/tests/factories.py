import factory
import factory.fuzzy
from factory.django import DjangoModelFactory

from conferences.tests.factories import ConferenceFactory
from i18n.tests.factories import LanguageFactory
from job_board.models import JobListing


class JobListingFactory(DjangoModelFactory):
    title = LanguageFactory("sentence")
    slug = LanguageFactory("slug")
    description = LanguageFactory("sentence")
    company = LanguageFactory("sentence")
    company_logo = factory.django.ImageField()
    conference = factory.SubFactory(ConferenceFactory)

    class Meta:
        model = JobListing

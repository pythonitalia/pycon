import factory

from pytest_factoryboy import register

from factory.django import DjangoModelFactory

from conferences.models import Conference


@register
class ConferenceFactory(DjangoModelFactory):
    class Meta:
        model = Conference

    name = factory.Faker('name')
    slug = factory.Faker('slug')

    start = factory.Faker('past_date')
    end = factory.Faker('future_date')

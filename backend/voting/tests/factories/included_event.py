import factory
from pytest_factoryboy import register

from conferences.tests.factories import ConferenceFactory
from voting.models import IncludedEvent


@register
class IncludedEventFactory(factory.django.DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)
    pretix_organizer_id = "another-organizer"
    pretix_event_id = "another-event"

    class Meta:
        model = IncludedEvent

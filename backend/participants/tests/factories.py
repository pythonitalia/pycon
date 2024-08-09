import factory
import factory.fuzzy
from factory.django import DjangoModelFactory

from conferences.tests.factories import ConferenceFactory
from participants.models import Participant


class ParticipantFactory(DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)
    user = factory.SubFactory("users.tests.factories.UserFactory")
    photo = (
        "https://marcopycontest.blob.core.windows.net/participants-avatars/blobblob.jpg"
    )
    bio = "bio bio"
    website = "http://google.it"
    twitter_handle = "handle"
    speaker_level = "intermediate"
    previous_talk_video = ""

    class Meta:
        model = Participant

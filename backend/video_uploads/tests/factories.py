from conferences.tests.factories import ConferenceFactory
import factory
from video_uploads.models import VideosImportRequest
from factory.django import DjangoModelFactory


class VideosImportRequestFactory(DjangoModelFactory):
    class Meta:
        model = VideosImportRequest

    conference = factory.SubFactory(ConferenceFactory)
    source_url = "https://wetransfer.com/downloads/fake_transfer_id/fake_security_code"

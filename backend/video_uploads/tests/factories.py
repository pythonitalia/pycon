from conferences.tests.factories import ConferenceFactory
import factory
from video_uploads.models import WetransferToS3TransferRequest
from factory.django import DjangoModelFactory


class WetransferToS3TransferRequestFactory(DjangoModelFactory):
    class Meta:
        model = WetransferToS3TransferRequest

    conference = factory.SubFactory(ConferenceFactory)
    wetransfer_url = (
        "https://wetransfer.com/downloads/fake_transfer_id/fake_security_code"
    )

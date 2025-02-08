from pathlib import Path
from users.tests.factories import UserFactory
from conferences.tests.factories import ConferenceFactory
from visa.models import (
    InvitationLetterAsset,
    InvitationLetterDocument,
    InvitationLetterRequest,
    InvitationLetterConferenceConfig,
    InvitationLetterRequestStatus,
)
import factory
import factory.fuzzy
from factory.django import DjangoModelFactory

BASE_EXAMPLE_DYNAMIC_DOCUMENT_JSON = {
    "header": {"content": "header", "margin": "0", "align": "top-left"},
    "footer": {"content": "footer", "margin": "0", "align": "top-left"},
    "page_layout": {"margin": "1cm 0 1cm 0"},
    "pages": [
        {
            "id": "id",
            "title": "title",
            "content": "content",
        }
    ],
}


class InvitationLetterRequestFactory(DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)
    requester = factory.SubFactory(UserFactory)
    date_of_birth = factory.Faker("date")
    full_name = factory.Faker("name")
    nationality = factory.Faker("country")
    address = factory.Faker("address")
    passport_number = factory.Faker("ssn")
    embassy_name = factory.Faker("company")

    class Meta:
        model = InvitationLetterRequest


class SentInvitationLetterRequestFactory(InvitationLetterRequestFactory):
    status = InvitationLetterRequestStatus.SENT
    invitation_letter = factory.django.FileField()


class InvitationLetterConferenceConfigFactory(DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)

    class Meta:
        model = InvitationLetterConferenceConfig


class InvitationLetterDocumentFactory(DjangoModelFactory):
    invitation_letter_conference_config = factory.SubFactory(
        InvitationLetterConferenceConfigFactory
    )
    document = factory.django.FileField(
        from_path=Path(__file__).parent / "fixtures" / "sample-pdf.pdf"
    )

    class Meta:
        model = InvitationLetterDocument


class InvitationLetterDynamicDocumentFactory(InvitationLetterDocumentFactory):
    document = None
    dynamic_document = BASE_EXAMPLE_DYNAMIC_DOCUMENT_JSON

    class Meta:
        model = InvitationLetterDocument


class InvitationLetterAssetFactory(DjangoModelFactory):
    invitation_letter_conference_config = factory.SubFactory(
        InvitationLetterConferenceConfigFactory
    )
    identifier = factory.Faker("md5")
    image = factory.django.ImageField()

    class Meta:
        model = InvitationLetterAsset

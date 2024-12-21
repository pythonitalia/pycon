from pathlib import Path
from users.tests.factories import UserFactory
from conferences.tests.factories import ConferenceFactory
from visa.models import (
    InvitationLetterAsset,
    InvitationLetterDocument,
    InvitationLetterRequest,
    InvitationLetterConferenceConfig,
)
import factory
import factory.fuzzy
from factory.django import DjangoModelFactory


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


class InvitationLetterAssetFactory(DjangoModelFactory):
    invitation_letter_conference_config = factory.SubFactory(
        InvitationLetterConferenceConfigFactory
    )
    identifier = factory.Faker("md5")
    image = factory.django.ImageField()

    class Meta:
        model = InvitationLetterAsset

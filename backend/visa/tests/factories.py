from pathlib import Path
from users.tests.factories import UserFactory
from conferences.tests.factories import ConferenceFactory
from organizers.tests.factories import OrganizerFactory
from visa.models import (
    InvitationLetterAsset,
    InvitationLetterDocument,
    InvitationLetterRequest,
    InvitationLetterOrganizerConfig,
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


class InvitationLetterOrganizerConfigFactory(DjangoModelFactory):
    organizer = factory.SubFactory(OrganizerFactory)

    class Meta:
        model = InvitationLetterOrganizerConfig


class InvitationLetterDocumentFactory(DjangoModelFactory):
    invitation_letter_organizer_config = factory.SubFactory(
        InvitationLetterOrganizerConfigFactory
    )
    document = factory.django.FileField(
        from_path=Path(__file__).parent / "fixtures" / "sample-pdf.pdf"
    )

    class Meta:
        model = InvitationLetterDocument


class InvitationLetterAssetFactory(DjangoModelFactory):
    invitation_letter_organizer_config = factory.SubFactory(
        InvitationLetterOrganizerConfigFactory
    )
    identifier = factory.Faker("md5")
    image = factory.django.ImageField()

    class Meta:
        model = InvitationLetterAsset

from conferences.tests.factories import ConferenceFactory
from pytest import mark

from i18n.strings import LazyI18nString
from conferences.models.conference import get_upload_to

pytestmark = mark.django_db


def test_conference_to_str():
    assert "Ciao Mondo <ep1>" == str(
        ConferenceFactory(name=LazyI18nString({"en": "Ciao Mondo"}), code="ep1")
    )


def test_upload_to():
    conference = ConferenceFactory()
    assert (
        get_upload_to(conference, "test.jpg")
        == f"conferences/{conference.code}/test.jpg"
    )

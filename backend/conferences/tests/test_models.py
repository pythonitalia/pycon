from conferences.tests.factories import ConferenceFactory
from pytest import mark

from i18n.strings import LazyI18nString


@mark.django_db
def test_conference_to_str():
    assert "Ciao Mondo <ep1>" == str(
        ConferenceFactory(name=LazyI18nString({"en": "Ciao Mondo"}), code="ep1")
    )

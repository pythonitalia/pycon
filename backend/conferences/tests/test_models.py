from pytest import mark

from i18n.strings import LazyI18nString


@mark.django_db
def test_conference_to_str(conference_factory):
    assert "Ciao Mondo <ep1>" == str(
        conference_factory(name=LazyI18nString({"en": "Ciao Mondo"}), code="ep1")
    )

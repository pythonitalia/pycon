import pytest
from i18n.strings import LazyI18nString
from pages.models import Page


@pytest.mark.django_db
def test_automatic_slug(page_factory):
    page = page_factory(slug=None)
    assert page.slug


@pytest.mark.django_db
def test_filter_by_slug(page_factory):
    slug_en = "demo"
    slug_it = "prova"

    page_factory(slug=LazyI18nString({"en": slug_en, "it": slug_it}), published=True)
    page_factory(published=True)

    assert Page.published_pages.by_slug(slug_it).count() == 1
    assert Page.published_pages.by_slug(slug_en).count() == 1

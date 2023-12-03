import pytest
from cms.components.page.tasks import revalidate_vercel_frontend_task
from cms.components.sites.tests.factories import VercelFrontendSettingsFactory
from wagtail_factories import PageFactory, SiteFactory

pytestmark = pytest.mark.django_db


def test_revalidate_vercel_frontend(
    requests_mock,
):
    site = SiteFactory()
    parent = PageFactory()
    page = PageFactory(slug="test-page123")
    page.set_url_path(parent)

    site.root_page = parent
    site.save()

    settings = VercelFrontendSettingsFactory(
        revalidate_url="https://test.com", revalidate_secret="test", site=site
    )
    mock_call = requests_mock.post(settings.revalidate_url, status_code=200)

    revalidate_vercel_frontend_task(page_id=page.id)

    assert mock_call.called
    body = mock_call.last_request.json()
    assert body["secret"] == "test"
    assert body["path"] == "/en/test-page123"


def test_revalidate_vercel_frontend_special_case_for_landing_page(
    requests_mock,
):
    site = SiteFactory()

    parent = PageFactory()
    page = PageFactory(slug=site.hostname)
    page.set_url_path(parent)
    site.root_page = parent

    site.save()

    settings = VercelFrontendSettingsFactory(
        revalidate_url="https://test.com", revalidate_secret="test", site=site
    )
    mock_call = requests_mock.post(settings.revalidate_url, status_code=200)

    revalidate_vercel_frontend_task(page_id=page.id)

    assert mock_call.called

    body = mock_call.last_request.json()
    assert body["secret"] == "test"
    assert body["path"] == "/en"


def test_revalidate_vercel_frontend_for_different_language(requests_mock, locale):
    parent = PageFactory()
    site = SiteFactory(hostname="pycon", root_page=parent)

    page = PageFactory(slug="test123", locale=locale("en"), parent=parent)
    page.set_url_path(parent)

    italian_page = page.copy_for_translation(locale=locale("it"))
    italian_page.slug = "something-else"
    italian_page.save()
    italian_page.set_url_path(parent)

    settings = VercelFrontendSettingsFactory(
        revalidate_url="https://test.com", revalidate_secret="test", site=site
    )
    mock_call = requests_mock.post(settings.revalidate_url, status_code=200)

    revalidate_vercel_frontend_task(page_id=italian_page.id)

    assert mock_call.called

    body = mock_call.last_request.json()
    assert body["secret"] == "test"
    assert body["path"] == "/it/test123"


def test_revalidate_vercel_frontend_when_vercel_is_down_doesnt_crash(
    caplog,
    requests_mock,
    locale,
):
    parent = PageFactory()

    page = PageFactory(slug="test123", locale=locale("en"), parent=parent)
    site = SiteFactory(hostname="pycon", root_page=page)

    italian_page = page.copy_for_translation(locale=locale("it"))
    italian_page.slug = "something-else"
    italian_page.save()

    settings = VercelFrontendSettingsFactory(
        revalidate_url="https://test.com", revalidate_secret="test", site=site
    )
    mock_call = requests_mock.post(settings.revalidate_url, status_code=500)

    revalidate_vercel_frontend_task(page_id=italian_page.id)

    assert mock_call.called
    assert "Error while revalidating" in caplog.records[0].message

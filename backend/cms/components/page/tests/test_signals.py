import json
import pytest
from cms.components.page.signals import revalidate_vercel_frontend
from cms.components.sites.tests.factories import VercelFrontendSettingsFactory
from wagtail_factories import PageFactory, SiteFactory

pytestmark = pytest.mark.django_db


def test_revalidate_vercel_frontend_disabled_if_not_configured(requests_mock):
    mock_call = requests_mock.post("https://test.com", status_code=200)

    site = SiteFactory()
    page = PageFactory()
    site.root_page = page
    site.save()
    revalidate_vercel_frontend("test_revalidate_vercel_frontend", instance=page)

    assert not mock_call.called


def test_revalidate_vercel_frontend(
    requests_mock,
):
    parent = PageFactory()
    page = PageFactory(slug="test-page123")
    page.set_url_path(parent)

    site = SiteFactory(root_page=parent)

    settings = VercelFrontendSettingsFactory(
        revalidate_url="https://test.com", revalidate_secret="test", site=site
    )
    mock_call = requests_mock.post(settings.revalidate_url, status_code=200)

    revalidate_vercel_frontend("test_revalidate_vercel_frontend", instance=page)

    assert mock_call.called

    body = json.loads(mock_call.calls[0].request.content)
    assert body["secret"] == "test"
    assert body["path"] == "/en/test-page123"


def test_revalidate_vercel_frontend_special_case_for_homepage(
    requests_mock,
):
    parent = PageFactory()
    page = PageFactory(slug="homepage")
    page.set_url_path(parent)

    site = SiteFactory(root_page=parent)

    settings = VercelFrontendSettingsFactory(
        revalidate_url="https://test.com", revalidate_secret="test", site=site
    )
    mock_call = requests_mock.post(settings.revalidate_url, status_code=200)

    revalidate_vercel_frontend("test_revalidate_vercel_frontend", instance=page)

    assert mock_call.called

    body = json.loads(mock_call.calls[0].request.content)
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

    revalidate_vercel_frontend("test_revalidate_vercel_frontend", instance=italian_page)

    assert mock_call.called

    body = json.loads(mock_call.calls[0].request.content)
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

    revalidate_vercel_frontend("test_revalidate_vercel_frontend", instance=italian_page)

    assert mock_call.called

    json.loads(mock_call.calls[0].request.content)
    assert "Error while revalidating" in caplog.records[0].message

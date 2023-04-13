import json
import pytest
from page.signals import revalidate_vercel_frontend


pytestmark = pytest.mark.django_db


def test_revalidate_vercel_frontend_disabled_if_not_configured(
    page_factory, site_factory, respx_mock
):
    mock_call = respx_mock.post("https://test.com").respond(status_code=200)

    site = site_factory()
    page = page_factory()
    site.root_page = page
    site.save()
    revalidate_vercel_frontend("test_revalidate_vercel_frontend", instance=page)

    assert not mock_call.called


def test_revalidate_vercel_frontend(
    page_factory, site_factory, respx_mock, vercel_frontend_settings_factory
):
    parent = page_factory()
    page = page_factory(slug="test-page123")
    page.set_url_path(parent)

    site = site_factory(root_page=parent)

    settings = vercel_frontend_settings_factory(
        revalidate_url="https://test.com", revalidate_secret="test", site=site
    )
    mock_call = respx_mock.post(settings.revalidate_url).respond(status_code=200)

    revalidate_vercel_frontend("test_revalidate_vercel_frontend", instance=page)

    assert mock_call.called

    body = json.loads(mock_call.calls[0].request.content)
    assert body["secret"] == "test"
    assert body["path"] == "/en/test-page123"


def test_revalidate_vercel_frontend_special_case_for_homepage(
    page_factory, site_factory, respx_mock, vercel_frontend_settings_factory
):
    parent = page_factory()
    page = page_factory(slug="homepage")
    page.set_url_path(parent)

    site = site_factory(root_page=parent)

    settings = vercel_frontend_settings_factory(
        revalidate_url="https://test.com", revalidate_secret="test", site=site
    )
    mock_call = respx_mock.post(settings.revalidate_url).respond(status_code=200)

    revalidate_vercel_frontend("test_revalidate_vercel_frontend", instance=page)

    assert mock_call.called

    body = json.loads(mock_call.calls[0].request.content)
    assert body["secret"] == "test"
    assert body["path"] == "/en"


def test_revalidate_vercel_frontend_for_different_language(
    page_factory, site_factory, respx_mock, vercel_frontend_settings_factory, locale
):
    parent = page_factory()
    site = site_factory(hostname="pycon", root_page=parent)

    page = page_factory(slug="test123", locale=locale("en"), parent=parent)
    page.set_url_path(parent)

    italian_page = page.copy_for_translation(locale=locale("it"))
    italian_page.slug = "something-else"
    italian_page.save()
    italian_page.set_url_path(parent)

    settings = vercel_frontend_settings_factory(
        revalidate_url="https://test.com", revalidate_secret="test", site=site
    )
    mock_call = respx_mock.post(settings.revalidate_url).respond(status_code=200)

    revalidate_vercel_frontend("test_revalidate_vercel_frontend", instance=italian_page)

    assert mock_call.called

    body = json.loads(mock_call.calls[0].request.content)
    assert body["secret"] == "test"
    assert body["path"] == "/it/test123"


def test_revalidate_vercel_frontend_when_vercel_is_down_doesnt_crash(
    caplog,
    page_factory,
    site_factory,
    respx_mock,
    vercel_frontend_settings_factory,
    locale,
):
    parent = page_factory()

    page = page_factory(slug="test123", locale=locale("en"), parent=parent)
    site = site_factory(hostname="pycon", root_page=page)

    italian_page = page.copy_for_translation(locale=locale("it"))
    italian_page.slug = "something-else"
    italian_page.save()

    settings = vercel_frontend_settings_factory(
        revalidate_url="https://test.com", revalidate_secret="test", site=site
    )
    mock_call = respx_mock.post(settings.revalidate_url).respond(status_code=500)

    revalidate_vercel_frontend("test_revalidate_vercel_frontend", instance=italian_page)

    assert mock_call.called

    json.loads(mock_call.calls[0].request.content)
    assert "Error while revalidating" in caplog.records[0].message

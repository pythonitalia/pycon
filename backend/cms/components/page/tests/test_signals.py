from unittest import mock
import pytest
from cms.components.page.signals import revalidate_vercel_frontend
from wagtail_factories import PageFactory, SiteFactory

pytestmark = pytest.mark.django_db


@mock.patch("cms.components.page.signals.revalidate_vercel_frontend_task")
def test_revalidate_vercel_frontend_disabled_if_not_configured(mock_task):
    site = SiteFactory()
    page = PageFactory()
    site.root_page = page
    site.save()

    revalidate_vercel_frontend("test_revalidate_vercel_frontend", instance=page)

    mock_task.delay.assert_not_called()


@mock.patch("cms.components.page.signals.revalidate_vercel_frontend_task")
def test_revalidate_vercel_frontend(mock_task):
    site = SiteFactory()
    page = PageFactory()
    site.root_page = page
    site.save()

    revalidate_vercel_frontend("test_revalidate_vercel_frontend", instance=page)

    mock_task.delay.assert_called_with(page_id=page.id)

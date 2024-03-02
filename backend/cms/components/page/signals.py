import logging

from cms.components.sites.models import VercelFrontendSettings
from cms.components.page.tasks import revalidate_vercel_frontend_task
from wagtail.models import Site

logger = logging.getLogger(__name__)


def revalidate_vercel_frontend(sender, **kwargs):
    instance = kwargs["instance"]

    try:
        site = instance.get_site()
    except Site.DoesNotExist:
        return

    if not site:
        return

    settings = VercelFrontendSettings.for_site(site)

    if not settings.revalidate_url:
        return

    revalidate_vercel_frontend_task.delay(page_id=instance.id)

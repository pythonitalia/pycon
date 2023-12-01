import logging

from cms.components.sites.models import VercelFrontendSettings
from cms.components.page.tasks import revalidate_vercel_frontend_task

logger = logging.getLogger(__name__)


def revalidate_vercel_frontend(sender, **kwargs):
    instance = kwargs["instance"]

    site = instance.get_site()
    if not site:
        # page doesn't belong to any site
        return

    settings = VercelFrontendSettings.for_site(site)

    if not settings:
        # not configured for this site
        return

    revalidate_vercel_frontend_task.delay(site_id=site.id, page_id=instance.id)

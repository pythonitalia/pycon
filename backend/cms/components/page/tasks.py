import requests
import logging
from pycon.celery import app
from wagtail.models import Page
from cms.components.sites.models import VercelFrontendSettings

logger = logging.getLogger(__name__)


@app.task
def revalidate_vercel_frontend_task(page_id):
    page = Page.objects.get(id=page_id)
    site = page.get_site()

    settings = VercelFrontendSettings.for_site(site)

    site_name = site.site_name
    hostname = site.hostname

    url = settings.revalidate_url
    secret = settings.revalidate_secret

    if not url or not secret:
        # not configured for this site
        return

    language_code = page.locale.language_code

    if language_code != "en":
        # we need to get the original slug
        # as we use the english slugs for the frontend
        english_page = (
            page.get_translations(inclusive=True)
            .filter(locale__language_code="en")
            .first()
        )

        slug = english_page.slug
        _, _, page_path = english_page.get_url_parts()
    else:
        slug = page.slug
        _, _, page_path = page.get_url_parts()

    page_path = page_path[:-1]

    if slug == hostname:
        path = f"/{language_code}"
    else:
        path = f"/{language_code}{page_path}"

    try:
        response = requests.post(
            url,
            timeout=None,
            json={
                "secret": secret,
                "path": path,
            },
        )
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Error while revalidating {path} on {site_name}: {e}")
        return

    logger.info(f"Revalidated {path} on {site_name}")

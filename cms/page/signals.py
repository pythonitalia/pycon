import httpx
import logging

from sites.models import VercelFrontendSettings

logger = logging.getLogger(__name__)


def revalidate_vercel_frontend(sender, **kwargs):
    instance = kwargs["instance"]

    site = kwargs["instance"].get_site()
    site_name = site.site_name
    settings = VercelFrontendSettings.for_site(site)

    if not settings:
        # not configured for this site
        return

    url = settings.revalidate_url
    secret = settings.revalidate_secret

    if not url or not secret:
        # not configured for this site
        return

    language_code = instance.locale.language_code

    if language_code != "en":
        # we need to get the original slug
        # as we use the english slugs for the frontend
        english_page = (
            instance.get_translations(inclusive=True)
            .filter(locale__language_code="en")
            .first()
        )

        slug = english_page.slug
    else:
        slug = instance.slug

    if slug == "homepage":
        path = f"/{language_code}"
    else:
        path = f"/{language_code}/{slug}"

    try:
        response = httpx.post(
            url,
            timeout=None,
            json={
                "secret": secret,
                "path": path,
            },
        )
        response.raise_for_status()
    except httpx.HTTPError as e:
        logger.error(f"Error while revalidating {path} on {site_name}: {e}")
        return

    logger.info(f"Revalidated {path} on {site_name}")

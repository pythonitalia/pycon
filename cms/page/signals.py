import httpx
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def revalidate_pycon_frontend(sender, **kwargs):
    secret = settings.REVALIDATE_SECRET
    frontend_url = settings.PYCON_FRONTEND_SERVICE

    if not secret:
        logger.debug("No secret set for revalidating pycon frontend")
        return

    if not frontend_url:
        logger.debug("No frontend url set for revalidating pycon frontend")
        return

    instance = kwargs["instance"]
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
            f"{frontend_url}/api/revalidate",
            timeout=None,
            json={
                "secret": secret,
                "path": path,
            },
        )
        response.raise_for_status()
    except httpx.HTTPError as e:
        logger.error(f"Error while revalidating {path} on pycon frontend: {e}")
        return

    logger.info(f"Revalidated {path} on pycon frontend")

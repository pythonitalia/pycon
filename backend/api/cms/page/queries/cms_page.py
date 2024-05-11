from api.cms.utils import get_site_by_host
from cms.components.page.models import GenericPage as GenericPageModel

import strawberry

from api.cms.page.types import GenericPage, SiteNotFoundError


@strawberry.field
def cms_page(
    hostname: str,
    slug: str,
    language: str,
    password: str | None = None,
) -> GenericPage | SiteNotFoundError | None:
    site = get_site_by_host(hostname)

    if not site:
        return SiteNotFoundError(message=f"Site `{hostname}` not found")

    page = GenericPageModel.objects.in_site(site).filter(slug=slug).first()
    password_restriction = (
        page.get_view_restrictions().filter(restriction_type="password").first()
    )

    if password_restriction and password_restriction.value != password:
        return None

    if not page:
        return None

    translated_page = (
        page.get_translations(inclusive=True)
        .filter(locale__language_code=language, live=True)
        .first()
    )

    if not translated_page:
        return None

    return GenericPage.from_model(translated_page)

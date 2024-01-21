from cms.components.page.models import GenericPage as GenericPageModel
from wagtail.models import Site

import strawberry

from api.cms.page.types import GenericPage, SiteNotFoundError


@strawberry.field
def cms_page(
    hostname: str,
    slug: str,
    language: str,
) -> GenericPage | SiteNotFoundError | None:
    hostname, port = hostname.split(":") if ":" in hostname else (hostname, 80)
    if not (site := Site.objects.filter(hostname=hostname, port=port).first()):
        return SiteNotFoundError(message=f"Site `{hostname}` not found")

    page = GenericPageModel.objects.in_site(site).filter(slug=slug).first()

    if not page:
        return None

    translated_page = (
        page.get_translations(inclusive=True)
        .filter(locale__language_code=language)
        .first()
    )

    if not translated_page:
        return None

    if not translated_page.live:
        return None
    return GenericPage.from_model(translated_page.live_revision.as_object())

from api.cms.utils import get_site_by_host
import strawberry
from cms.components.page.models import GenericPage as GenericPageModel

from api.cms.page.types import GenericPage


@strawberry.field
def cms_pages(hostname: str, language: str) -> list[GenericPage]:
    site = get_site_by_host(hostname)

    if not site:
        return []

    return [
        GenericPage.from_model(page)
        for page in GenericPageModel.objects.in_site(site).filter(
            locale__language_code=language, live=True
        )
    ]

import strawberry
from wagtail.models import Site
from cms.components.page.models import GenericPage as GenericPageModel

from api.cms.page.types import GenericPage


@strawberry.field
def cms_pages(hostname: str, language: str) -> list[GenericPage]:
    hostname, port = hostname.split(":") if ":" in hostname else (hostname, 80)

    if not (site := Site.objects.filter(hostname=hostname, port=port).first()):
        return []

    return [
        GenericPage.from_model(page)
        for page in GenericPageModel.objects.in_site(site).filter(
            locale__language_code=language, live=True
        )
    ]

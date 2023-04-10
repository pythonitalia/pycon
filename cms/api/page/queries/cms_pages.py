import strawberry
from wagtail.models import Site
from page.models import GenericPage as GenericPageModel

from api.page.types import GenericPage


@strawberry.field
def cms_pages(hostname: str, language: str) -> list[GenericPage]:
    if not (site := Site.objects.filter(hostname=hostname).first()):
        return []

    return [
        GenericPage.from_model(page)
        for page in GenericPageModel.objects.in_site(site).filter(
            locale__language_code=language,
        )
        if page.slug != "homepage"
    ]

from page.models import GenericPage as GenericPageModel

import strawberry
from api.page.types import GenericPage
from wagtail.models import Site


@strawberry.type
class SiteNotFoundError:
    message: str


@strawberry.type
class Query:
    @strawberry.field
    def cms_page(
        self,
        hostname: str,
        slug: str,
        language: str,
    ) -> GenericPage | SiteNotFoundError | None:
        if not (site := Site.objects.filter(hostname=hostname).first()):
            return SiteNotFoundError(message=f"Site `{hostname}` not found")

        page = GenericPageModel.objects.in_site(site).filter(slug=slug).first()

        if not page:
            return None

        translated_page = (
            page.get_translations(inclusive=True)
            .filter(locale__language_code=language)
            .first()
        )
        return GenericPage.from_model(translated_page)

    @strawberry.field
    def cms_pages(self, hostname: str, language: str) -> list[GenericPage]:
        if not (site := Site.objects.filter(hostname=hostname).first()):
            return []

        return [
            GenericPage.from_model(page)
            for page in GenericPageModel.objects.in_site(site).filter(
                locale__language_code=language
            )
        ]


schema = strawberry.federation.Schema(query=Query)

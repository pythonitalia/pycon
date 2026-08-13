from api.context import Info
import strawberry
import strawberry_django
from pages.models import Page

from .types import Page as PageType


@strawberry.type
class PagesQuery:
    # TODO: use custom scalar for code and update custom gatsby source to use
    # that instead of a generic argument called code

    @strawberry_django.field
    def pages(self, info: Info, code: str) -> list[PageType]:
        return Page.published_pages.filter(conference__code=code)

    @strawberry_django.field
    def page(self, info: Info, code: str, slug: str) -> PageType | None:
        return Page.published_pages.by_slug(slug).filter(conference__code=code).first()

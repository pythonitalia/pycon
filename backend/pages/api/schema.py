from api.context import Info
import strawberry
import strawberry_django
from pages import models

from .types import Page


@strawberry.type
class PagesQuery:
    # TODO: use custom scalar for code and update custom gatsby source to use
    # that instead of a generic argument called code

    @strawberry_django.field
    def pages(self, info: Info, code: str) -> list[Page]:
        return models.Page.published_pages.filter(conference__code=code)

    @strawberry_django.field
    def page(self, info: Info, code: str, slug: str) -> Page | None:
        return (
            models.Page.published_pages.by_slug(slug)
            .filter(conference__code=code)
            .first()
        )

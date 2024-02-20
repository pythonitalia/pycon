from typing import List, Optional

from api.context import Info
import strawberry
from pages.models import Page

from .types import Page as PageType


@strawberry.type
class PagesQuery:
    # TODO: use custom scalar for code and update custom gatsby source to use
    # that instead of a generic argument called code

    @strawberry.field
    def pages(self, info: Info, code: str) -> List[PageType]:
        return Page.published_pages.filter(conference__code=code)

    @strawberry.field
    def page(self, info: Info, code: str, slug: str) -> Optional[PageType]:
        return Page.published_pages.by_slug(slug).filter(conference__code=code).first()

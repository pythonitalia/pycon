from typing import List, Optional

import strawberry
from pages.models import Page

from .types import Page as PageType


@strawberry.type
class PagesQuery:
    # TODO: use custom scalar for code and update custom gatsby source to use
    # that instead of a generic argument called code

    @strawberry.field
    def pages(self, info, code: str) -> List[PageType]:
        return Page.published_pages.filter(conference__code=code)

    @strawberry.field
    def page(self, info, code: str, slug: str) -> Optional[PageType]:
        return Page.published_pages.filter(conference__code=code, slug=slug).first()

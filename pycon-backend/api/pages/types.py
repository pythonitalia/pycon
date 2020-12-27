from typing import Optional

import strawberry

from ..helpers.i18n import make_localized_resolver
from ..helpers.images import resolve_image


@strawberry.type
class Page:
    id: strawberry.ID
    title: str = strawberry.field(resolver=make_localized_resolver("title"))
    slug: str = strawberry.field(resolver=make_localized_resolver("slug"))
    content: str = strawberry.field(resolver=make_localized_resolver("content"))
    excerpt: Optional[str]
    image: Optional[str] = strawberry.field(resolver=resolve_image)

from typing import Optional

import strawberry

from ..helpers.i18n import make_localized_resolver


@strawberry.type
class Page:
    id: strawberry.ID
    title: str = strawberry.field(resolver=make_localized_resolver("title"))
    slug: str = strawberry.field(resolver=make_localized_resolver("slug"))
    content: str = strawberry.field(resolver=make_localized_resolver("content"))
    excerpt: Optional[str]

    @strawberry.field
    def image(self, info) -> Optional[str]:
        if not self.image:
            return None

        return info.context["request"].build_absolute_uri(self.image.url)

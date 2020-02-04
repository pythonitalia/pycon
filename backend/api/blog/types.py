from typing import Optional

import strawberry
from api.users.types import User
from strawberry.types.datetime import DateTime

from ..helpers.i18n import make_localized_resolver


@strawberry.type
class Post:
    id: strawberry.ID
    author: User
    title: str = strawberry.field(resolver=make_localized_resolver("title"))
    slug: str = strawberry.field(resolver=make_localized_resolver("slug"))
    excerpt: str = strawberry.field(resolver=make_localized_resolver("excerpt"))
    content: str = strawberry.field(resolver=make_localized_resolver("content"))
    published: DateTime

    @strawberry.field
    def image(self, info) -> Optional[str]:
        if not self.image:
            return None

        return info.context["request"].build_absolute_uri(self.image.url)

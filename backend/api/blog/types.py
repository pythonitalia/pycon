from typing import Optional

import strawberry
from api.scalars import DateTime
from api.users.types import User


@strawberry.type
class Post:
    id: strawberry.ID
    author: User
    title: str
    slug: str
    excerpt: Optional[str]
    content: Optional[str]
    published: DateTime

    @strawberry.field
    def image(self, info) -> Optional[str]:
        if not self.image:
            return None

        return info.context["request"].build_absolute_uri(self.image.url)

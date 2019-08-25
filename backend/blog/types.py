from typing import Optional

import strawberry
from api.scalars import DateTime
from users.types import UserType


@strawberry.type
class Post:
    id: strawberry.ID
    author: UserType
    title: str
    slug: str
    excerpt: Optional[str]
    content: Optional[str]
    published: DateTime

    @strawberry.field
    def image(self, info) -> Optional[str]:
        if not self.image:
            return None

        return info.context.build_absolute_uri(self.image.url)

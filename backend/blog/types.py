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
    image: Optional[str]

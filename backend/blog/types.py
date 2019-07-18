import strawberry

from users.types import UserType
from api.scalars import DateTime


@strawberry.type
class Post:
    author: UserType
    title: str
    slug: str
    excerpt: str
    content: str
    published: DateTime
    image: str

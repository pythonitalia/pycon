from datetime import datetime
from typing import Optional

import strawberry

from ..helpers.i18n import make_localized_resolver


@strawberry.type
class BlogPostAuthor:
    id: strawberry.ID
    full_name: str


@strawberry.type
class Post:
    id: strawberry.ID
    author: BlogPostAuthor
    title: str = strawberry.field(resolver=make_localized_resolver("title"))
    slug: str = strawberry.field(resolver=make_localized_resolver("slug"))
    excerpt: str = strawberry.field(resolver=make_localized_resolver("excerpt"))
    content: str = strawberry.field(resolver=make_localized_resolver("content"))
    image: Optional[str]
    published: datetime

    def __init__(
        self,
        id: strawberry.ID,
        author: BlogPostAuthor,
        title: str,
        slug: str,
        excerpt: str,
        content: str,
        published: datetime,
        image: Optional[str],
    ) -> None:
        self.id = id
        self.author = author
        self.title = title
        self.slug = slug
        self.excerpt = excerpt
        self.content = content
        self.published = published
        self.image = image

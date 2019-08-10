from typing import List, Optional

import strawberry

from .models import Post
from .types import Post as PostType


@strawberry.type
class BlogQuery:
    @strawberry.field
    def blog_posts(self, info) -> List[PostType]:
        return Post.published_posts.all()

    @strawberry.field
    def blog_post(self, info, slug: str) -> Optional[PostType]:
        return Post.published_posts.filter(slug=slug).first()

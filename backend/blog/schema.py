from typing import List

import strawberry

from .models import Post
from .types import Post as PostType


@strawberry.type
class BlogQuery:
    @strawberry.field
    def blog_posts(self, info) -> List[PostType]:
        return Post.published_posts.all()

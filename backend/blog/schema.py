import strawberry

from .types import Post as PostType
from .models import Post


@strawberry.query
class BlogQuery:
    def blog_posts(self, info) -> PostType:
        return Post.published_posts.all()

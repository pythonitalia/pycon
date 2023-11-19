from typing import List, Optional

import strawberry

from blog.models import Post

from .types import BlogPostAuthor
from .types import Post as PostType


@strawberry.type
class BlogQuery:
    @strawberry.field
    def blog_posts(self, info) -> List[PostType]:
        return [
            PostType(
                id=post.id,
                author=BlogPostAuthor(
                    id=post.author_id, full_name=post.author.full_name
                ),
                title=post.title,
                slug=post.slug,
                excerpt=post.excerpt,
                content=post.content,
                published=post.published,
                image=(
                    info.context.request.build_absolute_uri(post.image.url)
                    if post.image
                    else None
                ),
            )
            for post in Post.published_posts.all()
        ]

    @strawberry.field
    def blog_post(self, info, slug: str) -> Optional[PostType]:
        post = Post.published_posts.by_slug(slug).first()

        if not post:
            return None

        return PostType(
            id=post.id,
            author=BlogPostAuthor(id=post.author_id, full_name=post.author.full_name),
            title=post.title,
            slug=post.slug,
            excerpt=post.excerpt,
            content=post.content,
            published=post.published,
            image=info.context.request.build_absolute_uri(post.image.url)
            if post.image
            else None,
        )

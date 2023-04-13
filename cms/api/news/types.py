import datetime
from typing import Self
import strawberry


@strawberry.type
class NewsArticle:
    id: strawberry.ID
    title: str
    slug: str
    excerpt: str
    body: str
    published_at: datetime.datetime
    author_fullname: str

    @classmethod
    def from_model(cls, model) -> Self:
        return cls(
            id=model.id,
            title=model.title,
            slug=model.slug,
            excerpt=model.excerpt,
            body=model.body,
            published_at=model.first_published_at,
            author_fullname=model.owner.get_full_name(),
        )

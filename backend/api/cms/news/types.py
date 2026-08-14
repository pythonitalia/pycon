import datetime

import strawberry
import strawberry_django

from cms.components.news import models


@strawberry_django.type(models.NewsArticle)
class NewsArticle:
    id: strawberry.auto
    title: strawberry.auto
    slug: strawberry.auto
    excerpt: strawberry.auto
    body: str = strawberry_django.field(only=["body"])
    published_at: datetime.datetime | None = strawberry_django.field(
        field_name="first_published_at"
    )

    @strawberry_django.field(select_related=["owner"])
    def author_fullname(self) -> str:
        return self.owner.display_name if self.owner_id else ""

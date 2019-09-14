from typing import Optional

import strawberry
from django.conf import settings
from django.utils import translation


def make_localized_resolver(field_name: str):
    def resolver(root, info, language: Optional[str] = None) -> str:
        language = language or translation.get_language() or settings.LANGUAGE_CODE

        return getattr(root, field_name).localize(language)

    return resolver


@strawberry.type
class Page:
    id: strawberry.ID
    title: str = strawberry.field(resolver=make_localized_resolver("title"))
    slug: str = strawberry.field(resolver=make_localized_resolver("slug"))
    content: str = strawberry.field(resolver=make_localized_resolver("content"))
    excerpt: Optional[str]

    @strawberry.field
    def image(self, info) -> Optional[str]:
        if not self.image:
            return None

        return info.context["request"].build_absolute_uri(self.image.url)

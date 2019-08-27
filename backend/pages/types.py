from typing import Optional

import strawberry


@strawberry.type
class Page:
    id: strawberry.ID
    title: str
    slug: str
    excerpt: Optional[str]
    content: Optional[str]

    @strawberry.field
    def image(self, info) -> Optional[str]:
        if not self.image:
            return None

        return info.context.build_absolute_uri(self.image.url)

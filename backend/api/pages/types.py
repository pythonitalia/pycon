import strawberry_django
from pages.models import Page as PageModel
from strawberry import auto

from ..helpers.i18n import make_localized_resolver
from ..helpers.images import resolve_image


@strawberry_django.type(PageModel)
class Page:
    id: auto
    title: str = strawberry_django.field(
        resolver=make_localized_resolver("title"), only=["title"]
    )
    slug: str = strawberry_django.field(
        resolver=make_localized_resolver("slug"), only=["slug"]
    )
    content: str = strawberry_django.field(
        resolver=make_localized_resolver("content"), only=["content"]
    )
    excerpt: str | None = strawberry_django.field(
        resolver=lambda root: getattr(root, "excerpt", None),
        disable_optimization=True,
    )
    image: str | None = strawberry_django.field(
        resolver=resolve_image, only=["image"]
    )

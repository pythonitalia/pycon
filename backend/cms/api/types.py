import strawberry
import strawberry_django

from pages.api.types import Page
from cms import models

from api.helpers.i18n import make_localized_resolver


@strawberry.type
class FAQ:
    id: strawberry.ID
    question: str = strawberry.field(resolver=make_localized_resolver("question"))
    answer: str = strawberry.field(resolver=make_localized_resolver("answer"))


@strawberry_django.type(models.MenuLink)
class MenuLink:
    href: str = strawberry_django.field(
        resolver=make_localized_resolver("href"), only=["href"]
    )
    title: str = strawberry_django.field(
        resolver=make_localized_resolver("title"), only=["title"]
    )
    is_primary: strawberry.auto
    page: Page | None


@strawberry_django.type(models.Menu)
class Menu:
    title: str = strawberry_django.field(
        resolver=make_localized_resolver("title"), only=["title"]
    )
    links: list[MenuLink]

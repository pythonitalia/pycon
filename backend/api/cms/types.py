import strawberry
from strawberry import ID

from api.context import Info

from ..helpers.i18n import make_localized_resolver


@strawberry.type
class FAQ:
    id: ID
    question: str = strawberry.field(resolver=make_localized_resolver("question"))
    answer: str = strawberry.field(resolver=make_localized_resolver("answer"))


@strawberry.type
class MenuLink:
    href: str = strawberry.field(resolver=make_localized_resolver("href"))
    title: str = strawberry.field(resolver=make_localized_resolver("title"))
    is_primary: bool


@strawberry.type
class Menu:
    title: str = strawberry.field(resolver=make_localized_resolver("title"))

    @strawberry.field
    def links(self, info: Info) -> list[MenuLink]:
        return self.links.all()

import typing

import strawberry
from api.pages.types import Page

from ..helpers.i18n import make_localized_resolver


@strawberry.type
class FAQ:
    question: str = strawberry.field(resolver=make_localized_resolver("question"))
    answer: str = strawberry.field(resolver=make_localized_resolver("answer"))


@strawberry.type
class MenuLink:
    href: str = strawberry.field(resolver=make_localized_resolver("href"))
    title: str = strawberry.field(resolver=make_localized_resolver("title"))
    is_primary: bool
    page: typing.Optional[Page]


@strawberry.type
class Menu:
    title: str = strawberry.field(resolver=make_localized_resolver("title"))

    @strawberry.field
    def links(self, info) -> typing.List[MenuLink]:
        return self.links.all()

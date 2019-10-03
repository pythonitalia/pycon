import typing

import strawberry

from ..helpers.i18n import make_localized_resolver


@strawberry.type
class FAQ:
    question: str = strawberry.field(resolver=make_localized_resolver("question"))
    answer: str = strawberry.field(resolver=make_localized_resolver("answer"))


@strawberry.type
class MenuLink:
    href: str
    title: str
    target: typing.Optional[str]


@strawberry.type
class Menu:
    @strawberry.field
    def links(self, info) -> typing.List[MenuLink]:
        return self.links.all()

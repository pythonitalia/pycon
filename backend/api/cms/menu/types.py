from typing import Self
from strawberry import ID
import strawberry
from wagtailmenus.models import MainMenu, FlatMenu


@strawberry.type
class CMSMenuItem:
    id: ID
    title: str

    @classmethod
    def from_model(cls, item) -> Self:
        return cls(
            id=item.id,
            title=item.title,
        )


@strawberry.type
class CMSMenu:
    id: ID
    title: str
    items: list[CMSMenuItem]

    @classmethod
    def from_model(cls, menu: MainMenu | FlatMenu) -> Self:
        title = menu.title if isinstance(menu, FlatMenu) else "Main"

        return cls(
            id=menu.id,
            title=title,
            items=[CMSMenuItem.from_model(item) for item in menu.items],
        )

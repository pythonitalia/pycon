from typing import Self
from api.cms.page.registry import register_page_block
import strawberry


@register_page_block
@strawberry.type
class HomeIntroSection:
    id: strawberry.ID
    pretitle: str
    title: str

    @classmethod
    def from_block(cls, block) -> Self:
        return cls(
            id=block.id,
            pretitle=block.value["pretitle"],
            title=block.value["title"],
        )

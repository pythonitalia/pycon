from typing import Self
import strawberry
from api.cms.page.registry import register_page_block
import enum


@strawberry.enum
class DynamicContentDisplaySectionSource(enum.Enum):
    speakers = "speakers"
    keynoters = "keynoters"
    proposals = "proposals"
    communities = "communities"


@register_page_block()
@strawberry.type
class DynamicContentDisplaySection:
    id: strawberry.ID
    source: DynamicContentDisplaySectionSource

    @classmethod
    def from_block(cls, block) -> Self:
        return cls(
            id=block.id,
            source=DynamicContentDisplaySectionSource(block.value["source"]),
        )

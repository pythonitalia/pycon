import datetime
from typing import Self
from api.cms.page.registry import register_page_block
import strawberry

from api.cms.base.blocks.cta import CTA


@register_page_block()
@strawberry.type
class InformationSection:
    id: strawberry.ID
    title: str
    body: str
    illustration: str
    background_color: str
    countdown_to_datetime: datetime.datetime | None
    countdown_to_deadline: str | None
    cta: CTA | None

    @classmethod
    def from_block(cls, block) -> Self:
        cta = block.value["cta"]
        return cls(
            id=block.id,
            title=block.value["title"],
            body=block.value["body"],
            illustration=block.value["illustration"],
            background_color=block.value["background_color"],
            countdown_to_datetime=block.value["countdown_to_datetime"],
            countdown_to_deadline=block.value["countdown_to_deadline"],
            cta=CTA.from_block(cta) if cta["label"] else None,
        )

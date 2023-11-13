from typing import Self
import strawberry

from api.cms.base.blocks.cta import CTA


@strawberry.type
class SchedulePreviewSection:
    id: strawberry.ID
    title: str
    primary_cta: CTA | None
    secondary_cta: CTA | None

    @classmethod
    def from_block(cls, block) -> Self:
        primary_cta = block.value["primary_cta"]
        secondary_cta = block.value["secondary_cta"]

        return cls(
            id=block.id,
            title=block.value["title"],
            primary_cta=(CTA.from_block(primary_cta) if primary_cta["label"] else None),
            secondary_cta=(
                CTA.from_block(secondary_cta) if secondary_cta["label"] else None
            ),
        )

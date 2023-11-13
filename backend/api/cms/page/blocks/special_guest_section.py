import datetime
from typing import Any
import strawberry

from api.cms.base.blocks.cta import CTA


@strawberry.type
class SpecialGuestSection:
    id: strawberry.ID
    title: str
    guest_name: str
    guest_job_title: str
    event_date: datetime.date
    cta: CTA | None
    _block: strawberry.Private[Any]

    @strawberry.field
    def guest_photo(self) -> str:
        guest_photo = self._block.value["guest_photo"]
        return guest_photo.get_rendition("fill-600x600|jpegquality-60").full_url

    @classmethod
    def from_block(cls, block):
        cta = block.value["cta"]
        return cls(
            id=block.id,
            title=block.value["title"],
            guest_name=block.value["guest_name"],
            guest_job_title=block.value["guest_job_title"],
            event_date=block.value["event_date"],
            cta=CTA.from_block(cta) if cta["label"] else None,
            _block=block,
        )

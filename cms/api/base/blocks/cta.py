from typing import Self
import strawberry


@strawberry.type
class CTA:
    label: str
    link: str

    @classmethod
    def from_block(cls, block) -> Self:
        return cls(label=block["label"], link=block["link"])

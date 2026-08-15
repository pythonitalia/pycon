from typing import Self
import strawberry


@strawberry.type
class Accordion:
    title: str
    body: str
    is_open: bool

    @classmethod
    def from_block(cls, block) -> Self:
        return cls(
            title=block["title"],
            body=block["body"],
            is_open=block["is_open"],
        )

from typing import Self
import strawberry


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

from typing import Self
import strawberry


@strawberry.type
class SocialsSection:
    id: strawberry.ID
    label: str
    hashtag: str

    @classmethod
    def from_block(cls, block) -> Self:
        return cls(
            id=block.id,
            label=block.value["label"],
            hashtag=block.value["hashtag"],
        )
